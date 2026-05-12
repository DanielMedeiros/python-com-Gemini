"""
Cliente Gemini Personalizado - Otimizado para seus modelos disponíveis
Baseado na detecção: 10 modelos funcionais encontrados
"""

import os
import time
from typing import Optional, List, Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    """
    Cliente Gemini otimizado com os modelos da sua conta
    """
    
    # Modelos disponíveis organizados por categoria (baseado na sua detecção)
    MODELOS = {
        # Modelos principais (mais rápidos e econômicos)
        'rapido': 'models/gemini-2.5-flash',           # Gemini 2.5 Flash
        'rapido_lite': 'models/gemini-2.5-flash-lite', # Gemini 2.5 Flash-Lite
        'flash_latest': 'models/gemini-flash-latest',  # Última versão Flash
        'flash_lite_latest': 'models/gemini-flash-lite-latest', # Flash-Lite mais recente
        
        # Modelos experimentais (mais avançados)
        'experimental': 'models/gemini-3.1-flash-lite-preview', # Preview 3.1
        'futuro': 'models/gemini-3-flash-preview',     # Gemini 3 Preview
        'pro_lite': 'models/gemini-3.1-flash-lite',    # 3.1 Flash Lite
        
        # Modelos especializados
        'gemma_26b': 'models/gemma-4-26b-a4b-it',     # Gemma 4 26B
        'gemma_31b': 'models/gemma-4-31b-it',         # Gemma 4 31B
        'robotica': 'models/gemini-robotics-er-1.6-preview', # Robótica
        
        # Aliases fáceis de lembrar
        'padrao': 'models/gemini-2.5-flash',
        'melhor': 'models/gemini-2.5-flash',
        'economico': 'models/gemini-2.5-flash-lite',
    }
    
    def __init__(self, api_key: Optional[str] = None, modelo_preferido: str = 'padrao'):
        """
        Inicializa o cliente Gemini
        
        Args:
            api_key: Chave da API (opcional, usa .env)
            modelo_preferido: 'padrao', 'rapido', 'experimental', 'gemma_31b', etc.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("API Key não encontrada! Configure no .env")
        
        self.client = genai.Client(api_key=self.api_key)
        
        # Define o modelo a usar
        self.modelo_atual = self.MODELOS.get(modelo_preferido, self.MODELOS['padrao'])
        
        print(f" Cliente Gemini otimizado!")
        print(f" Modelo: {self.modelo_atual}")
        print(f" {len(self.MODELOS)} modelos disponíveis para uso")
    
    def listar_meus_modelos(self):
        """
        Mostra todos os modelos disponíveis na sua conta
        """
        print("\n SEUS MODELOS DISPONÍVEIS:")
        print("="*50)
        
        categorias = {
            " Rápidos e Econômicos": ['rapido', 'rapido_lite', 'flash_latest', 'flash_lite_latest'],
            " Experimentais": ['experimental', 'futuro', 'pro_lite'],
            " Especializados": ['gemma_26b', 'gemma_31b', 'robotica']
        }
        
        for categoria, modelos in categorias.items():
            print(f"\n{categoria}:")
            for nome in modelos:
                modelo = self.MODELOS[nome]
                status = " ATUAL" if modelo == self.modelo_atual else "  "
                print(f"  {status} • {nome:20} → {modelo}")
    
    def mudar_modelo(self, modelo_nome: str):
        """
        Troca o modelo ativo
        
        Args:
            modelo_nome: Nome do modelo (ex: 'gemma_31b', 'experimental', 'rapido')
        """
        if modelo_nome in self.MODELOS:
            self.modelo_atual = self.MODELOS[modelo_nome]
            print(f" Modelo alterado para: {self.modelo_atual}")
        else:
            print(f" Modelo '{modelo_nome}' não encontrado!")
            print("Use um destes:", ', '.join(self.MODELOS.keys()))
    
    def gerar_texto(
        self, 
        prompt: str, 
        temperatura: float = 0.7,
        max_tokens: int = 1000,
        modelo: Optional[str] = None
    ) -> str:
        """
        Gera texto com controle de parâmetros
        
        Args:
            prompt: Texto de entrada
            temperatura: Criatividade (0.0 = determinístico, 1.0 = criativo)
            max_tokens: Máximo de tokens na resposta
            modelo: Modelo específico (opcional)
        
        Returns:
            Texto gerado
        """
        try:
            modelo_usar = self.MODELOS.get(modelo, self.modelo_atual) if modelo else self.modelo_atual
            
            response = self.client.models.generate_content(
                model=modelo_usar,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperatura,
                    max_output_tokens=max_tokens,
                )
            )
            return response.text
        except Exception as e:
            erro_str = str(e)
            if "429" in erro_str:
                return "⏳ Limite de requisições. Aguarde um momento..."
            return f" Erro: {erro_str[:100]}"
    
    def gerar_creativo(self, prompt: str) -> str:
        """Geração com alta criatividade (ideal para brainstorm)"""
        return self.gerar_texto(prompt, temperatura=0.9, max_tokens=2000)
    
    def gerar_preciso(self, prompt: str) -> str:
        """Geração precisa e determinística (ideal para fatos)"""
        return self.gerar_texto(prompt, temperatura=0.1, max_tokens=500)
    
    def gerar_com_modelo_grande(self, prompt: str) -> str:
        """Usa o modelo mais potente disponível (Gemma 31B)"""
        return self.gerar_texto(prompt, modelo='gemma_31b', max_tokens=2000)
    
    def iniciar_chat(self, instrucao: Optional[str] = None, modelo: str = 'padrao'):
        """
        Inicia uma conversa
        
        Args:
            instrucao: Instrução do sistema (contexto/personalidade)
            modelo: Modelo a usar no chat
        
        Returns:
            Sessão de chat
        """
        config = None
        if instrucao:
            config = types.GenerateContentConfig(
                system_instruction=instrucao
            )
        
        modelo_usar = self.MODELOS.get(modelo, self.modelo_atual)
        
        return self.client.chats.create(
            model=modelo_usar,
            config=config
        )
    
    def comparar_modelos(self, prompt: str, modelos: List[str] = None):
        """
        Compara respostas de diferentes modelos
        
        Args:
            prompt: Pergunta para testar
            modelos: Lista de modelos para comparar (ex: ['rapido', 'gemma_31b'])
        """
        if not modelos:
            modelos = ['rapido', 'experimental', 'gemma_26b']
        
        print(f"\n COMPARANDO MODELOS")
        print("="*50)
        print(f"Prompt: {prompt}\n")
        
        for modelo_nome in modelos:
            print(f" {modelo_nome} ({self.MODELOS[modelo_nome]}):")
            print("-"*40)
            
            inicio = time.time()
            resposta = self.gerar_texto(prompt, modelo=modelo_nome)
            fim = time.time()
            
            print(resposta[:200])
            print(f"⏱ Tempo: {fim - inicio:.2f}s")
            print()


class ChatInterativo:
    """
    Chat interativo com múltiplos modelos
    """
    
    def __init__(self):
        self.cliente = GeminiClient()
        self.chat_atual = None
        self.historico = []
    
    def iniciar(self):
        """Inicia o chat interativo"""
        print("\n CHAT GEMINI INTERATIVO")
        print("="*50)
        print("Comandos especiais:")
        print("  /modelos    - Listar seus modelos")
        print("  /mudar NOME - Trocar modelo (ex: /mudar gemma_31b)")
        print("  /comparar   - Comparar modelos com última pergunta")
        print("  /criativo   - Modo criativo")
        print("  /preciso    - Modo preciso")
        print("  /limpar     - Nova conversa")
        print("  /sair       - Encerrar")
        print("="*50)
        
        while True:
            try:
                entrada = input("\n Você: ").strip()
                
                if not entrada:
                    continue
                
                # Comandos
                if entrada.startswith('/'):
                    self._processar_comando(entrada)
                    continue
                
                # Chat normal
                if not self.chat_atual:
                    self.chat_atual = self.cliente.iniciar_chat()
                
                print(" Pensando...", end="\r")
                resposta = self.chat_atual.send_message(entrada)
                self.historico.append((entrada, resposta.text))
                
                print(f" Gemini: {resposta.text}\n")
                
            except KeyboardInterrupt:
                print("\n Até logo!")
                break
            except Exception as e:
                print(f" Erro: {e}")
    
    def _processar_comando(self, comando: str):
        """Processa comandos do chat"""
        cmd = comando.lower()
        
        if cmd == '/sair':
            print(" Até logo!")
            exit()
        elif cmd == '/modelos':
            self.cliente.listar_meus_modelos()
        elif cmd.startswith('/mudar'):
            partes = cmd.split()
            if len(partes) > 1:
                self.cliente.mudar_modelo(partes[1])
                self.chat_atual = None  # Reinicia chat
        elif cmd == '/criativo':
            print(" Modo criativo ativado!")
        elif cmd == '/preciso':
            print(" Modo preciso ativado!")
        elif cmd == '/limpar':
            self.chat_atual = None
            self.historico = []
            print(" Nova conversa iniciada!")
        elif cmd == '/comparar' and self.historico:
            ultima_pergunta = self.historico[-1][0]
            self.cliente.comparar_modelos(ultima_pergunta)
        else:
            print(" Comando não reconhecido")


# Demonstração rápida
def demonstracao():
    """Mostra as capacidades do sistema"""
    print(" DEMONSTRAÇÃO GEMINI PERSONALIZADO")
    print("="*60)
    
    cliente = GeminiClient()
    
    # Mostra modelos
    cliente.listar_meus_modelos()
    
    # Teste com diferentes estilos
    print("\n TESTES DE GERAÇÃO:")
    
    # Preciso
    print("\n1⃣ Modo Preciso:")
    print(cliente.gerar_preciso("Qual a capital da França? (responda apenas o nome)"))
    
    # Criativo
    print("\n2⃣ Modo Criativo:")
    print(cliente.gerar_creativo("Crie um slogan para uma empresa de IA"))
    
    # Modelo grande
    print("\n3⃣ Modelo Avançado (Gemma 31B):")
    print(cliente.gerar_com_modelo_grande("Explique computação quântica em 2 frases"))
    
    print("\n Demonstração concluída!")
    print("\n Para iniciar o chat interativo: python chat_avancado.py")


if __name__ == "__main__":
    demonstracao()