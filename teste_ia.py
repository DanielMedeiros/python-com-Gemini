"""
Teste rápido da integração Gemini
"""

from gemini_client import testar_conexao, GeminiSimples

def teste_rapido():
    """Executa um teste rápido"""
    print("="*50)
    print(" TESTE RÁPIDO GEMINI")
    print("="*50)
    
    # Testa conexão
    cliente = testar_conexao()
    
    if cliente:
        print("\n" + "="*50)
        print(" Integração funcionando perfeitamente!")
        print("="*50)
        
        # Exemplo de uso
        print("\n Exemplo de uso:")
        ai = GeminiSimples()
        
        perguntas = [
            "O que é Python?",
            "Qual a diferença entre lista e tupla?",
            "Explique o que é um dicionário"
        ]
        
        for pergunta in perguntas:
            print(f"\n Pergunta: {pergunta}")
            resposta = ai.perguntar(pergunta)
            print(f" Resposta: {resposta[:200]}...")

if __name__ == "__main__":
    teste_rapido()