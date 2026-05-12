# Gemini — Guia rápido de uso

Este README descreve como configurar e usar o projeto. Cobre primeiro o `setup.sh`, depois o módulo `gemini_client.py` e, por fim, como usar o `chat_avancado.py`.

**Pré-requisitos**

- Python 3.10+ instalado no sistema
- Acesso à internet para instalar dependências
- Arquivo `requirements.txt` presente na raiz do projeto
- Defina sua chave de API no arquivo `.env` como `GEMINI_API_KEY=sua_chave`

**1) Setup (script `setup.sh`)**
O arquivo [setup.sh](setup.sh) automatiza a criação de um ambiente virtual e a instalação das dependências.

Executar no Linux / macOS / Git Bash:

```bash
./setup.sh
# ou
bash setup.sh
```

No Windows (PowerShell) você pode usar estes passos equivalentes:

```powershell
# cria venv (nome sugerido: .venv)
python -m venv .venv
# ativa o venv (PowerShell)
.\.venv\Scripts\Activate.ps1
# ou (cmd)
.\.venv\Scripts\activate.bat
# instala dependências
pip install -r requirements.txt
```

Observação: o `setup.sh` do repositório cria um venv chamado `venv`. É comum usar `.venv` (com ponto); ambos funcionam, escolha um e mantenha consistente.

---

**2) `gemini_client.py` — como usar**
O arquivo [gemini_client.py](gemini_client.py) contém a classe `GeminiClient` e utilitários de chat. Configure sua chave no `.env` ou passe `api_key` ao construir o cliente.

Exemplo mínimo de uso em Python:

```python
from gemini_client import GeminiClient

# opcional: passar api_key explicitamente
cliente = GeminiClient(api_key=None)  # usa GEMINI_API_KEY do .env

# listar modelos
cliente.listar_meus_modelos()

# gerar texto simples
resposta = cliente.gerar_texto("Explique o que é Python em 2 frases.")
print(resposta)

# modos auxiliares
criativo = cliente.gerar_creativo("Crie um slogan para uma startup de IA")
preciso = cliente.gerar_preciso("Qual é a capital da França?")

# iniciar sessão de chat programaticamente
chat = cliente.iniciar_chat(instrucao="Você é um assistente útil.")
# use a API do chat retornada conforme o SDK (ex: chat.send_message(...))
```

Classes e métodos úteis:

- `GeminiClient(api_key=None, modelo_preferido='padrao')` — inicializa o cliente
- `listar_meus_modelos()` — exibe modelos disponíveis
- `mudar_modelo(nome)` — altera o modelo ativo (use os aliases definidos)
- `gerar_texto(prompt, temperatura=0.7, max_tokens=1000, modelo=None)` — gera texto
- `gerar_creativo(prompt)` / `gerar_preciso(prompt)` — atalhos com parâmetros prontos
- `iniciar_chat(instrucao=None, modelo='padrao')` — inicia uma sessão de chat

---

**3) `chat_avancado.py` — execução do chat interativo**
O arquivo [chat_avancado.py](chat_avancado.py) fornece um menu interativo que usa `GeminiClient` e `ChatInterativo`.

Para rodar:

```bash
# ative seu ambiente virtual antes
python chat_avancado.py
```

No menu você encontrará opções para:

- Abrir o chat interativo
- Comparar respostas entre modelos
- Listar seus modelos
- Executar um teste rápido
- Rodar a demonstração completa

Use as teclas/entradas no terminal conforme o menu apresentado.

---

**Notas finais e boas práticas**

- Sempre mantenha sua `GEMINI_API_KEY` privada (arquivo `.env` não deve ser commitado em repositórios públicos).
- Se precisar recriar o ambiente virtual, exclua `venv` ou `.venv` e execute o passo de criação novamente.
- Caso ocorram problemas com dependências após remoção automática de emojis em arquivos, recrie o venv e reinstale:

```powershell
# exemplo Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
