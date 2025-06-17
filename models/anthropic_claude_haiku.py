import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

# Carrega o ID do modelo da variável de ambiente
ANTHROPIC_CLAUDE_HAIKU_MODEL_ID = os.getenv('ANTHROPIC_CLAUDE_HAIKU_MODEL_ID')

class AnthropicClaudeHaiku:
    def __init__(self, prompt, file_path=None, max_tokens=60_000):
        """
        Construtor da classe AnthropicClaudeSonnet para configurar o modelo de NLP
        
        Args:
            prompt (str): Texto de entrada para o modelo
            file_path (str): Caminho do arquivo a ser carregado (opcional)
            max_tokens (int): Limite máximo de tokens (padrão: 100,000)
        """
        self.max_tokens = max_tokens
        self.model_id = ANTHROPIC_CLAUDE_HAIKU_MODEL_ID
        
        # Carrega o arquivo se fornecido
        self.file_content = None
        self.file_name = None
        if file_path:
            self.load_file(file_path)
        
        # Configura a mensagem
        self.content = self.set_content(prompt)
        
        print(f"[DEBUG][SONNET] Foundation Model ID: {self.model_id}")
        print(f"[DEBUG][SONNET] Request body configurado com sucesso")

    def load_file(self, file_path):
        """
        Carrega arquivo como texto ou base64
        
        Args:
            file_path (str): Caminho do arquivo a ser carregado
        """
        try:
            self.file_name = os.path.basename(file_path)
            
            # Para arquivos de texto
            if file_path.lower().endswith(('.csv', '.txt', '.json')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.file_content = f.read()
            
            # Para arquivos binários (imagens, PDF, etc.)
            else:
                with open(file_path, 'rb') as f:
                    self.file_content = base64.b64encode(f.read()).decode('utf-8')
            
            print(f"[DEBUG][SONNET] Arquivo carregado: {self.file_name}")
            
        except Exception as e:
            print(f"[ERROR] Erro ao carregar o arquivo: {str(e)}")
            self.file_content = None
            self.file_name = None
            raise e

    def set_content(self, prompt):
        """
        Constrói o conteúdo da mensagem
        
        Args:
            prompt (str): Texto de entrada para o modelo
        
        Returns:
            list: Lista com o conteúdo da mensagem
        """
        content = [{"type": "text", "text": prompt}]
        
        # Adiciona arquivo se carregado
        if self.file_content and self.file_name:
            # Para arquivos de texto
            if isinstance(self.file_content, str) and self.file_name.lower().endswith(('.csv', '.txt', '.json')):
                content.append({
                    "type": "text",
                    "text": f"\n\nConteúdo do arquivo {self.file_name}:\n{self.file_content}"
                })
            
            # Para imagens
            elif self.file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": self._get_media_type(self.file_name),
                        "data": self.file_content
                    }
                })
        
        return content

    def _get_media_type(self, filename):
        """
        Determina o media type da imagem baseado na extensão
        
        Args:
            filename (str): Nome do arquivo
            
        Returns:
            str: Media type da imagem
        """
        extension = filename.lower().split('.')[-1]
        media_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        return media_types.get(extension, 'image/jpeg')

    def get_request_body(self):
        """
        Retorna o corpo da requisição no formato JSON especificado
        
        Returns:
            dict: Corpo da requisição completo
        """
        return {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": self.content
                    }
                ]
            }

    def get_request_body_json(self):
        """
        Retorna o corpo da requisição como string JSON
        
        Returns:
            str: Corpo da requisição em formato JSON
        """
        return json.dumps(self.get_request_body(), indent=2)

    def get_model_id(self):
        """
        Retorna o ID do modelo
        
        Returns:
            str: ID do modelo
        """
        return self.model_id