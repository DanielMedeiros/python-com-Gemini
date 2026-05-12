"""
detecta_modelos.py - Descobre quais modelos funcionam na sua conta
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def detectar_modelos_funcionais():
    """Detecta todos os modelos que realmente funcionam"""
    
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    
    print(" DETECTANDO MODELOS DISPONÍVEIS")
    print("="*60)
    
    # Lista todos os modelos disponíveis
    print("\n Todos os modelos listados pela API:")
    print("-"*40)
    
    modelos_validos = []
    
    for modelo in client.models.list():
        # Verifica se suporta geração de texto
        if "generateContent" in modelo.supported_actions:
            print(f"\n Nome: {modelo.name}")
            print(f"   Display: {modelo.display_name}")
            print(f"   Descrição: {modelo.description[:100]}")
            
            # Tenta usar o modelo para confirmar
            try:
                print(f"    Testando...", end=" ")
                resposta = client.models.generate_content(
                    model=modelo.name,
                    contents="Diga 'OK' em português"
                )
                print(f" FUNCIONA! Resposta: {resposta.text}")
                modelos_validos.append({
                    'nome': modelo.name,
                    'display': modelo.display_name,
                    'testado': True
                })
            except Exception as e:
                print(f" FALHOU: {str(e)[:80]}")
                modelos_validos.append({
                    'nome': modelo.name,
                    'display': modelo.display_name,
                    'testado': False,
                    'erro': str(e)[:100]
                })
    
    # Resumo final
    print("\n" + "="*60)
    print(" RESUMO DOS MODELOS FUNCIONAIS:")
    print("-"*40)
    
    funcionais = [m for m in modelos_validos if m.get('testado')]
    nao_funcionais = [m for m in modelos_validos if not m.get('testado')]
    
    if funcionais:
        print(f"\n {len(funcionais)} MODELOS FUNCIONANDO:")
        for m in funcionais:
            print(f"   • {m['nome']} ({m['display']})")
    else:
        print("\n NENHUM MODELO FUNCIONAL ENCONTRADO!")
    
    if nao_funcionais:
        print(f"\n {len(nao_funcionais)} MODELOS COM ERRO:")
        for m in nao_funcionais:
            print(f"   • {m['nome']}: {m.get('erro', 'Erro desconhecido')[:80]}")
    
    # Recomendação
    if funcionais:
        print(f"\n RECOMENDAÇÃO: Use o modelo: {funcionais[0]['nome']}")
    else:
        print("\n POSSÍVEIS PROBLEMAS:")
        print("1. API Key inválida ou expirada")
        print("2. Região não suportada (tente usar VPN)")
        print("3. Conta sem permissões adequadas")
        print("\n SOLUÇÕES:")
        print("• Crie uma nova API Key em: https://aistudio.google.com/apikey")
        print("• Verifique se há billing configurado (mesmo free tier)")
        print("• Tente com outra conta Google")
    
    return modelos_validos

if __name__ == "__main__":
    modelos = detectar_modelos_funcionais()