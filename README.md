# Remobilize on RD Bot

[🇵🇧 Português](#português) | [🇬🇧 English](#english)

---

<a id="português"></a>
## 📖 Português

### O que é o Bot Remobilize On RD?

O **remobilize_on_rd.py** é um bot automatizado desenvolvido para otimizar a comunicação entre o comandante e os engenheiros em partidas de Hell Let Loose. Ele substitui o comando manual `!rd` por um sistema automático que escuta o chat do jogo e dispara alertas em tempo real.

### Como Funciona?

O bot funciona através de um sistema de *hooks* que se integra ao CRCON (Community Run Console). Aqui está o fluxo:

1. **Monitoramento**: O bot escuta continuamente o chat do jogo através do hook `@on_chat`
2. **Detecção**: Quando o comandante digita `!rd`, o bot identifica o comando
3. **Acionamento**: Uma mensagem é automaticamente enviada

### Casos de Uso

- **Bombardeios**: Após um bombardeio aéreo do inimigo destruir os nodes defensivos
- **Sincronização**: Garante que toda a equipe de engenheiros receba o alerta simultaneamente

### Instalação

#### 1. Copiar o arquivo

Copie o arquivo `remobilize_on_rd.py` para a pasta `custom_tools/` do seu CRCON:

```bash
cp remobilize_on_rd.py custom_tools/
```

#### 2. Editar o arquivo de hooks

Edite o arquivo `hooks.py` para incluir a importação e o hook do bot:

```python
import custom_tools.remobilize_on_rd as remobilize

@on_chat
def remobilize_on_rd_chat(rcon, log):
    remobilize.on_chat_remobilize(rcon, log)
```

#### 3. Reiniciar o CRCON

Reinicie o CRCON usando o script fornecido:

```bash
./restart.sh
```

Ou reinicie manualmente o serviço CRCON.

### Como Usar

Durante a partida, o comandante simplesmente digita no chat do jogo:

```
!rd
```

Instantaneamente, todos os engenheiros receberão uma mensagem privada solicitando que remontem os nodes defensivos. Não há necessidade de repetir comandos ou aguardar confirmações.

### Requisitos

- CRCON instalado e em funcionamento
- Acesso ao arquivo `hooks.py`
- Acesso à pasta `custom_tools/`
- Permissões de escrita no diretório do CRCON

### Estrutura do Projeto

```
remobilize_on_rd/
├── custom_tools/
│   └── remobilize_on_rd.py    # Arquivo principal do bot
├── restart.sh                  # Script para reiniciar CRCON
└── README.md                   # Este arquivo
```

### Vantagens

✅ **Automatização**: Elimina a necessidade de comandos manuais repetitivos  
✅ **Eficiência**: Reduz o tempo de resposta da equipe de engenheiros  
✅ **Consistência**: Garante que todos recebam a mesma mensagem  
✅ **Integração**: Funciona perfeitamente com o CRCON existente  
✅ **Simplicidade**: Fácil instalação e configuração  

### Licença

MIT

---

<a id="english"></a>
## 📖 English

### What is the Remobilize On RD Bot?

The **remobilize_on_rd.py** is an automated bot designed to optimize communication between the Commander and Engineers in Hell Let Loose matches. It replaces the manual `!rd` command with an automatic system that listens to the game chat and triggers alerts in real-time.

### How It Works?

The bot operates through a *hooks* system that integrates with CRCON (Community Run Console). Here's the workflow:

1. **Monitoring**: The bot continuously listens to game chat through the `@on_chat` hook
2. **Detection**: When the commander types `!rd`, the bot identifies the command
3. **Triggering**: A message is automatically sent t

### Use Cases

- **Airstrikes**: After enemy airstrikes destroy defensive nodes
- **Synchronization**: Ensures the entire engineering team receives the alert simultaneously

### Installation

#### 1. Copy the file

Copy the `remobilize_on_rd.py` file to the `custom_tools/` folder of your CRCON:

```bash
cp remobilize_on_rd.py custom_tools/
```

#### 2. Edit the hooks file

Edit the `hooks.py` file to include the bot import and hook:

```python
import custom_tools.remobilize_on_rd as remobilize

@on_chat
def remobilize_on_rd_chat(rcon, log):
    remobilize.on_chat_remobilize(rcon, log)
```

#### 3. Restart CRCON

Restart CRCON using the provided script:

```bash
./restart.sh
```

Or restart the CRCON service manually.

### How to Use

During the match, the commander simply types in the game chat:

```
!rd
```

Instantly, all engineers will receive a private message requesting them to remobilize the defensive nodes. There's no need to repeat commands or wait for confirmations.

### Requirements

- CRCON installed and running
- Access to the `hooks.py` file
- Access to the `custom_tools/` folder
- Write permissions in the CRCON directory

### Project Structure

```
remobilize_on_rd/
├── custom_tools/
│   └── remobilize_on_rd.py    # Main bot file
├── restart.sh                  # Script to restart CRCON
└── README.md                   # This file
```

### Advantages

✅ **Automation**: Eliminates the need for repetitive manual commands  
✅ **Efficiency**: Reduces the response time of the engineering team  
✅ **Consistency**: Ensures everyone receives the same message  
✅ **Integration**: Works seamlessly with existing CRCON  
✅ **Simplicity**: Easy installation and configuration  

### License

MIT
