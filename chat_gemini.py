"""
Chat interativo com o novo SDK Gemini
"""

import sys
from gemini_client import GeminiSimples

def chat_interativo():
    """Chat interativo no terminal"""
    print("\n CHAT GEMINI INTERATIVO")
    print("="*40)
    print("Comandos:")
    print("  /limpar - Nova conversa")
    print("  /modelos - Listar modelos")
    print("  /sair - Encerrar")
    print("="*40)
    
    ai = GeminiSimples()
    
    while True:
        try:
            entrada = input("\n Você: ").strip()
            
            if not entrada:
                continue
            
            # Comandos especiais
            if entrada.lower() == '/sair':
                print(" Até logo!")
                break
            elif entrada.lower() == '/limpar':
                ai.chat = None
                print(" Nova conversa iniciada!")
                continue
            elif entrada.lower() == '/modelos':
                from gemini_client import GeminiClient
                GeminiClient().listar_modelos()
                continue
            
            # Envia mensagem
            print(" Pensando...", end="\r")
            resposta = ai.conversar(entrada)
            print(f" Gemini: {resposta}\n")
            
        except KeyboardInterrupt:
            print("\n Chat encerrado!")
            break
        except Exception as e:
            print(f" Erro: {e}")
            print("Tente novamente...")

if __name__ == "__main__":
    chat_interativo()