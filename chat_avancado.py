"""
Chat Gemini Avançado - Com todos os seus modelos
"""

from gemini_client import ChatInterativo, GeminiClient

def menu_principal():
    """Menu principal do sistema"""
    print("\n SISTEMA GEMINI PERSONALIZADO")
    print("="*40)
    print("1.  Chat Interativo")
    print("2.  Comparar Modelos")
    print("3.  Listar Meus Modelos")
    print("4.  Teste Rápido")
    print("5.  Demonstração Completa")
    print("0. Sair")
    print("="*40)
    
    return input("Escolha: ").strip()

if __name__ == "__main__":
    cliente = GeminiClient()
    
    while True:
        opcao = menu_principal()
        
        if opcao == '1':
            chat = ChatInterativo()
            chat.iniciar()
        
        elif opcao == '2':
            prompt = input("\nDigite o prompt para comparar: ")
            cliente.comparar_modelos(prompt)
        
        elif opcao == '3':
            cliente.listar_meus_modelos()
        
        elif opcao == '4':
            print("\n Teste Rápido:")
            resposta = cliente.gerar_texto("Diga olá em português!")
            print(f" {resposta}")
        
        elif opcao == '5':
            from gemini_client import demonstracao
            demonstracao()
        
        elif opcao == '0':
            print(" Até logo!")
            break
        
        else:
            print(" Opção inválida!")