"""
remobilize_on_rd.py

Plugin simples para CRCON (Hell Let Loose) que:
 - escuta mensagens de chat
 - quando um jogador digita "!rd" aplica um punish para forçar morte/respawn
 - protege contra spam com cooldown por jogador
 - tenta usar métodos da API Rcon quando disponíveis e tem fallback para enviar a string RCON crua

Compatível com Rcon v2 / hll_rcon_tool recentes: tenta várias variantes de método antes de usar exec plain string.
"""

from datetime import datetime, timedelta
from typing import Final

from rcon.rcon import Rcon, StructuredLogLineWithMetaData
from rcon.utils import get_server_number

# -------- CONFIGURAÇÃO --------
ENABLE_ON_SERVERS: Final = ["1"]     # servidores onde o plugin roda (mesma convenção do live_topstats)
CHAT_COMMAND: Final = "!rd"          # comando no chat
COOLDOWN_SECONDS: Final = 30         # cooldown por jogador
NOTIFY_PLAYER: Final = True          # enviar mensagem privada confirmando a ação
CONFIRM_MESSAGE: Final = "Remobilização solicitada — você será respawnado em instantes."  # mensagem ao jogador
PUNISH_REASON: Final = "Remobilize via !rd"
PUNISH_TYPES = ("suicide") 
# -------------------------------

# controle simples de cooldown (memória em processo)
_last_used: dict[str, datetime] = {}


def _now():
    return datetime.utcnow()


def _is_enabled_on_server() -> bool:
    server_number = get_server_number()
    return str(server_number) in ENABLE_ON_SERVERS


def _can_use(player_id: str) -> bool:
    last = _last_used.get(player_id)
    if not last:
        return True
    return ( _now() - last ).total_seconds() >= COOLDOWN_SECONDS


def _set_used(player_id: str):
    _last_used[player_id] = _now()


def _try_punish_via_api(rcon: Rcon, player_id_or_name: str) -> tuple[bool, str]:
    """
    Tenta várias formas de chamar o punish usando métodos Python expostos pela instância Rcon.
    Retorna (sucesso: bool, resposta_str).
    """
    tried = []
    # tenta métodos comuns
    candidate_methods = [
        ("punish_player", (player_id_or_name, "suicide", PUNISH_REASON)),
        ("punish", (player_id_or_name, "suicide", PUNISH_REASON)),
        ("PunishPlayer", (player_id_or_name, "suicide", PUNISH_REASON)),
        ("punish_player_by_id", (player_id_or_name, "suicide", PUNISH_REASON)),
        ("execute", (f'PunishPlayer {player_id_or_name} suicide "{PUNISH_REASON}"',)),
        ("run_command", (f'PunishPlayer {player_id_or_name} suicide "{PUNISH_REASON}"',)),
        ("rcon", (f'PunishPlayer {player_id_or_name} suicide "{PUNISH_REASON}"',)),
    ]

    for name, args in candidate_methods:
        if hasattr(rcon, name):
            try:
                fn = getattr(rcon, name)
                # se for callable, chama e retorna
                if callable(fn):
                    res = fn(*args)
                    return True, f"Called {name} -> {res}"
            except Exception as ex:
                tried.append(f"{name}: ERROR {ex}")
                # e continua para tentar outra alternativa

    # nada com métodos diretos deu certo
    return False, "no-api-method-found; tried: " + ", ".join(tried)


def _try_punish_via_exec(rcon: Rcon, player_id_or_name: str) -> tuple[bool, str]:
    """
    Fallback: constrói string RCON e tenta executar com métodos genéricos (execute/run_command/rcon.exec).
    """
    cmd_variants = []
    # tentar combinações de tipo
    for t in PUNISH_TYPES:
        cmd_variants.append(f'PunishPlayer {player_id_or_name} {t} "{PUNISH_REASON}"')
        cmd_variants.append(f'punishPlayer {player_id_or_name} {t} "{PUNISH_REASON}"')
        cmd_variants.append(f'punish {player_id_or_name} {t} "{PUNISH_REASON}"')

    # possíveis métodos executores
    executor_names = ["execute", "run_command", "send", "exec", "rcon", "execute_raw"]
    for cmd in cmd_variants:
        for exe in executor_names:
            if hasattr(rcon, exe) and callable(getattr(rcon, exe)):
                try:
                    fn = getattr(rcon, exe)
                    res = fn(cmd)
                    return True, f"Executed via {exe}: {res}"
                except Exception as ex:
                    # tenta próximo executor
                    continue

    # última tentativa: se Rcon fornecer do_run_commands style, montar dict (compatibilidade com do_run_commands)
    try:
        from rcon.rcon import do_run_commands  # pode existir no ambiente
        commands = { "PunishPlayer": { "cmd": [cmd_variants[0]] } }
        try:
            do_run_commands(rcon, commands)
            return True, "Executed via do_run_commands fallback"
        except Exception:
            pass
    except Exception:
        pass

    return False, "exec fallback failed"


def remobilize_on_chat(rcon: Rcon, struct_log: StructuredLogLineWithMetaData):
    """
    Handler a ser conectado ao evento `on_chat`.
    Usa os mesmos campos presentes em live_topstats e hooks.py: sub_content, player_id_1, player_name_1.
    """
    # somente roda se plugin habilitado no servidor
    if not _is_enabled_on_server():
        return

    chat_message = (struct_log.get("sub_content") or "").strip()
    if not chat_message:
        return

    # só responde exatamente ao comando (sem argumentos)
    if chat_message.lower() != CHAT_COMMAND.lower():
        return

    player_id = struct_log.get("player_id_1")
    player_name = struct_log.get("player_name_1") or str(player_id or "unknown")

    if not player_id:
        # sem id não conseguimos fazer message_player nem punish confiavelmente
        return

    # cooldown
    if not _can_use(player_id):
        try:
            rcon.message_player(player_id=player_id, message=f"Aguarde {COOLDOWN_SECONDS}s entre usos de {CHAT_COMMAND}.", save_message=False)
        except Exception:
            pass
        return

    _set_used(player_id)

    # confirmação ao jogador
    if NOTIFY_PLAYER:
        try:
            rcon.message_player(player_id=player_id, message=CONFIRM_MESSAGE, save_message=False)
        except Exception:
            # ignora se message_player não existir
            pass

    # tenta executar punish por API direta
    success, info = _try_punish_via_api(rcon, player_id)
    if not success:
        # tenta fallback via exec strings
        success2, info2 = _try_punish_via_exec(rcon, player_id)
        info = info + " | " + info2

    # log local para debug (vai para stdout/arquivo de logs do CRCON)
    try:
        # se Rcon tem logger use-o, senão print
        import logging
        logging.getLogger(__name__).info("remobilize: player=%s id=%s success=%s info=%s", player_name, player_id, success or success2, info)
    except Exception:
        print("remobilize:", player_name, player_id, success or success2, info)
