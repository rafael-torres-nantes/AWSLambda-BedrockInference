import os
import json
from dotenv import load_dotenv

# Importar as classes de serviços necessárias para a Lambda Function
from services.bedrock_services import BedrockInferenceService

# Importar as classes de modelos necessárias para a Lambda Function
from models.amazon_nova_pro import AmazonNovaPro
from models.anthropic_claude_haiku import AnthropicClaudeHaiku
from models.anthropic_claude_sonnet import AnthropicClaudeSonnet

# Importar as classes de templates necessárias para a Lambda Function
from templates.prompt_template import PromptTemplate 

# Importar as classes do controlodar necessárias para a Lambda Function
from controllers.token_manager import TokenManager

load_dotenv()

# Obtém o nome do bucket do S3 do arquivo .env
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# ============================================================================
# Função Lambda para inferência de modelos de NLP e armazenamento no DynamoDB
# ----------------------------------------------------------------------------
def lambda_handler(event, context):

    # 1 - Imprime o evento recebido
    print('*********** Start Lambda ***************') 
    print(f'[DEBUG] Event: {event}') 


    # 2 - Dicionário para armazenar os resultados da inferência
    data_models = {} 
    
    try:
        # 3 - Cria um contexto para o prompt
        context = event.get('context', None)

        # 4 - Gera o prompt para o modelo de NLP
        prompt = PromptTemplate(context) 
        print(f'[DEBUG] O prompt gerado: {prompt.get_prompt_text()}') 

        # 5 - Instancia a classe TokenManager
        token_manager = TokenManager(context_path=None, prompt=prompt.get_prompt_text())
        batch_file_path = token_manager.get_batch_path()

        # 6 - Instancia o modelo Amazon Nova Pro, e obtém o ID do modelo e o corpo da requisição
        novapro_model = AmazonNovaPro(prompt.get_prompt_text(), batch_file_path)
        print(f'[DEBUG] O tamanho do corpo da requisição para Nova Pro: {token_manager.count_tokens(str(novapro_model.get_request_body()))}')
        
        # 7 - Realiza a inferência do modelo de NLP para o modelo Amazon Nova Pro
        model_id = novapro_model.get_model_id()
        request_body = novapro_model.get_request_body()
        print(f'[DEBUG] O ID do modelo é: {model_id}')
        print(f'[DEBUG] O corpo da requisição é: {request_body}')

        # 8 - Realiza a inferência do modelo de NLP para o modelo Amazon Nova Pro
        response_novapro_model = BedrockInferenceService(model_id, request_body).invoke_model()
        print(f'[DEBUG] O resultado da inferência é: {response_novapro_model}') 

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Arquivo processado e salvo com sucesso.',
                'data': data_models,
            }),
        }
    
    except Exception as e:
        print(f'[ERROR] {e}') 
        return {
            'statusCode': 500, 
            'body': json.dumps({ 
                'error': str(e), 
                'message': 'Erro ao processar arquivos' 
            })
        }

lambda_handler({

  "status": "success",
  "folder": "+16472038405",
  "lines": 1,
  "output_key": "+16472038405/output.jsonl"
}, None)  # Chamada de teste para a função lambda_handler