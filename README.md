## Bot remobilize_on_rd.py


Este bot escuta o chat e detecta quando o comandante digita `!rd`. Quando acionado:
- Envia uma mensagem para os engenheiros solicitando que remontem os nodes após um bombardeio ou remoção.
- Utiliza a mesma estrutura de ganchos `@on_chat` do `hooks.py`.


### Instalação do remobilize_on_rd.py


1. Copie o arquivo `remobilize_on_rd.py` para a pasta `custom_tools/` do CRCON:
```bash
cp remobilize_on_rd.py custom_tools/
```


2. Edite o `hooks.py` para incluir o seguinte:
```python
import custom_tools.remobilize_on_rd as remobilize


@on_chat
def remobilize_on_rd_chat(rcon, log):
remobilize.on_chat_remobilize(rcon, log)
```


3. Reinicie o CRCON:
```bash
./restart.sh
```


### Comando no jogo
No chat do jogo, o comandante pode usar:
```
!rd
```
E os engenheiros receberão uma mensagem direta solicitando remobilização de nodos.


## Licença
MIT
