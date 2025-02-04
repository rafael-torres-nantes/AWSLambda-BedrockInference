# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# RUN LOCALY
from utils.check_aws import AWS_SERVICES

aws_services = AWS_SERVICES()

session = aws_services.login_session_AWS()
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import json
import boto3
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obtem-se o ID do foundation model a partir das variáveis de ambiente
CLAUDE_MODEL_ID = os.getenv('CLAUDE_MODEL_ID') # ID do modelo Claude para geração de texto

class BedrockInference:
    def __init__(self):
        """
        Inicializa o serviço AWS Bedrock.

        Cria uma sessão do Boto3 e um cliente para o serviço Bedrock, com a região configurada como 'us-east-1'.
        """

        # Inicializa o cliente do Bedrock Runtime
        self.bedrock_client = session.client('bedrock-runtime')

    # --------------------------------------------------------------------
    # Função que gera o corpo da requisição para o Bedrock
    # --------------------------------------------------------------------
    def generate_request_body(self, prompt):
        """
        Gera o corpo da requisição para enviar ao modelo Bedrock.

        Inclui o prompt e configurações de geração de texto como o número máximo de tokens, temperatura e topP.

        Returns:
            str: O corpo da requisição em formato JSON.
        """
        # Define a estrutura de mensagens para o modelo
        messages = [
            { "role" : 'user',
                "content": [
                    {'type' : 'text',
                    'text': prompt  # Usa o prompt fornecido como conteúdo de texto
                    }
                ]
            }
        ]
        
        # Define os parâmetros de geração, incluindo tokens máximos e parâmetros de temperatura
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4086,
            "messages": messages,
            "temperature": 0.2,  # Temperatura: controla a aleatoriedade da geração
            "top_p": 0.9  # top_p: controla a inclusão dos tokens mais prováveis
        }
        return json.dumps(request_body)  # Retorna o corpo da requisição em formato JSON

    # --------------------------------------------------------------------
    # Função que invoca o modelo e retorna a resposta gerada
    # --------------------------------------------------------------------
    def invoke_model(self, prompt):
        """
        Invoca o modelo Bedrock com o prompt fornecido.

        :param prompt: O prompt gerado que será enviado ao modelo.
        :return: Resposta de texto gerada pelo modelo.
        """
        # Invoca o modelo Bedrock com o corpo da requisição gerado
        response = self.bedrock_client.invoke_model(
            modelId=CLAUDE_MODEL_ID, 
            contentType='application/json',
            accept='application/json',
            body=self.generate_request_body(prompt)  # Gera o corpo da requisição
        )

        # Lê o corpo da resposta e extrai o texto gerado pelo modelo
        response_body = json.loads(response.get('body').read())
        response_text = response_body.get('content')[0]['text']

        return response_text  # Retorna o texto gerado