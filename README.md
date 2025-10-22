🪖 Remobilize On RD — Bot de Remobilização para Hell Let Loose
📘 Descrição

Remobilize On RD é um plugin para o CRCON (Community RCON Tool) do Hell Let Loose.
Ele permite que qualquer jogador digite o comando !rd no chat do jogo para se remobilizar instantaneamente, forçando a morte do personagem e permitindo que ele renasça no spawn desejado.

O bot aplica o comando RCON PunishPlayer <id> suicide — o mesmo usado pela comunidade — e foi otimizado para agir o mais rápido possível, disparando múltiplas tentativas em milissegundos (“burst mode”) para garantir resposta imediata do servidor.

⚙️ Como Funciona

O plugin escuta todas as mensagens de chat do servidor.

Quando detecta um jogador digitando !rd, ele:

Verifica se o servidor está habilitado (ENABLE_ON_SERVERS).

Garante que o jogador não esteja em cooldown (anti-spam).

Envia o comando RCON PunishPlayer <player_id> suicide imediatamente.

Dispara tentativas extras (em intervalos de milissegundos) para reduzir atrasos causados pelo servidor.

(Opcional) Envia uma mensagem privada ao jogador confirmando a remobilização.

O servidor executa o comando e o jogador é morto, podendo então selecionar um novo ponto de respawn.

⏱️ O delay restante (geralmente 2–5 segundos para a morte + ~10 segundos para selecionar respawn) é parte da mecânica do Hell Let Loose e não pode ser alterado via RCON.

🚀 Instalação
1. Pré-requisitos

CRCON (Community RCON Tool) já instalado e funcional.

Pasta de custom tools ativada (onde ficam os outros bots, como o live_topstats.py).

Python 3.10+.

2. Coloque o arquivo do plugin

Salve o arquivo remobilize_on_rd.py em:

<seu_crcon>/custom_tools/remobilize_on_rd.py


Se a pasta custom_tools não tiver um __init__.py, crie um arquivo vazio com esse nome:

<seu_crcon>/custom_tools/__init__.py

3. Configure o hooks.py

Abra o arquivo hooks.py e adicione as linhas abaixo:

import custom_tools.remobilize_on_rd as remobilize_on_rd

@on_chat
def remobilize_onchat(rcon: Rcon, struct_log):
    remobilize_on_rd.remobilize_on_chat(rcon, struct_log)


Salve o arquivo e reinicie o CRCON.

4. Teste no jogo

Entre no servidor e digite !rd no chat.

Você deverá receber a mensagem:
Remobilização solicitada — você será respawnado em instantes.

Em 2–5 segundos, seu personagem morrerá e poderá escolher um novo spawn.

🧠 Configurações Principais

As opções ficam no topo do arquivo remobilize_on_rd.py:

Variável	Padrão	Descrição
ENABLE_ON_SERVERS	["1"]	Lista de servidores onde o plugin roda
CHAT_COMMAND	"!rd"	Comando de chat para remobilizar
COOLDOWN_SECONDS	30	Tempo de espera entre usos (por jogador)
NOTIFY_PLAYER	True	Envia mensagem privada de confirmação
CONFIRM_MESSAGE	"Remobilização solicitada..."	Texto da mensagem privada
PUNISH_REASON	"Remobilize via !rd"	Texto que aparece no log de punição
PUNISH_VARIANTS	("suicide","kill")	Tipos de punição tentados
BURST_ATTEMPTS	3	Quantidade de tentativas rápidas
BURST_INTERVAL_MS	250	Intervalo (ms) entre as tentativas
⚡ Dicas

Execute o CRCON na mesma máquina ou rede do servidor para menor latência.

O comando !rd funciona apenas em servidores listados em ENABLE_ON_SERVERS.

Se quiser mudar o comando, altere CHAT_COMMAND = "!redeploy" (por exemplo).

Você pode duplicar o plugin para criar outras funções rápidas de admin.

🧩 Exemplo de Log
[INFO] remobilize burst fired: player_id=123456 attempts=3 interval_ms=250
[INFO] Executed via run_command: PunishPlayer 123456 suicide "Remobilize via !rd"

🪙 Créditos

Desenvolvido com base no projeto hll_rcon_tool de MarechJ
.

Adaptado e otimizado para bots CRCON por ChatGPT (assistente técnico) e [seu nome/a tag do projeto].

Agradecimentos à comunidade de administradores Hell Let Loose BR por testes e feedback.

🧰 Licença

Este plugin é distribuído sob a licença MIT — livre para uso, modificação e redistribuição, desde que mantidos os créditos originais.
