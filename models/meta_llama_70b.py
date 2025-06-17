import os
import json
from dotenv import load_dotenv

load_dotenv()

# Carrega o ID do modelo da variável de ambiente
CLAUDE_SONNET_MODEL_ID = os.getenv('META_LLAMA_70B_MODEL_ID')

class MetaLlama70b:

    def __init__(self, prompt):
        # 1 - Inicializa a variável do ID do modelo
        self.model_id = "meta.llama3-3-70b-instruct-v1:0"

        # 2 - Define o body da requisição que será enviada para o modelo
        self.request_body = self.set_request_body(prompt)    
    
    def get_model_id(self):
        """
        Função que retorna o ID do modelo de soneto de Claude Sonnet
        """
        return self.model_id
    
    
    def set_request_body(self, prompt):
        """
        Função que define o corpo da requisição que será enviada para o modelo

        Args:
            prompt (str): Prompt que será enviado para o modelo
        
        Returns:
            str: Corpo da requisição em formato JSON
        """
        
        # Define os parâmetros de geração, incluindo tokens máximos e parâmetros de temperatura
        self.request_body  = {
            "max_tokens": 2048,
            "messages": prompt,
            "temperature": 0.2,  # Temperatura: controla a aleatoriedade da geração
            "top_p": 0.9  # top_p: controla a inclusão dos tokens mais prováveis
        }
        return json.dumps(self.request_body)  # Retorna o corpo da requisição em formato JSON

    def get_request_body(self):
        """
        Função que retorna o corpo da requisição que será enviada para o modelo
        """
        return self.request_body
    
    