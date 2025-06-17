# AWS Lambda - Bedrock Inference com Modelos de IA

## 👨‍💻 Projeto desenvolvido por: 
[Rafael Torres Nantes](https://github.com/rafael-torres-nantes)

## Índice

* 📚 Contextualização do projeto
* 🛠️ Tecnologias/Ferramentas utilizadas
* 🖥️ Funcionamento do sistema
   * 🧩 AWS Lambda Handler
   * 🤖 Modelos de IA Suportados
   * 📊 Gerenciamento de Tokens
* 🔀 Arquitetura da aplicação
* 📁 Estrutura do projeto
* ⚙️ Configuração e variáveis de ambiente
* 📌 Como executar o projeto
* 🎯 Funcionalidades de inferência
* 🕵️ Dificuldades Encontradas

---

## 📚 Contextualização do projeto

O projeto **AWSLambda-BedrockInference** é uma solução serverless desenvolvida para **inferência de modelos de IA generativa** utilizando **AWS Bedrock**. O sistema foi projetado para processar prompts através de múltiplos modelos de IA, incluindo Amazon Nova Pro, Anthropic Claude Haiku e Claude Sonnet, gerando respostas inteligentes e precisas.

A aplicação funciona como uma **AWS Lambda Function** que orquestra chamadas para diferentes modelos de IA, aplicando técnicas avançadas de **prompt engineering** e **gerenciamento de tokens** para otimizar o desempenho e os custos.

## 🛠️ Tecnologias/Ferramentas utilizadas

[<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/AWS_Lambda-FF9900?logo=awslambda&logoColor=white">](https://aws.amazon.com/lambda/)
[<img src="https://img.shields.io/badge/AWS_Bedrock-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/bedrock/)
[<img src="https://img.shields.io/badge/Amazon_Nova_Pro-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/bedrock/)
[<img src="https://img.shields.io/badge/Anthropic_Claude-000000?logo=anthropic&logoColor=white">](https://www.anthropic.com/)
[<img src="https://img.shields.io/badge/Boto3-0073BB?logo=amazonaws&logoColor=white">](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[<img src="https://img.shields.io/badge/Visual_Studio_Code-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/dotenv-ECD53F?logo=dotenv&logoColor=black">](https://pypi.org/project/python-dotenv/)
[<img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white">](https://github.com/)

## 🖥️ Funcionamento do sistema

### 🧩 AWS Lambda Handler

O core da aplicação está no lambda_handler.py, que orquestra todo o processo de inferência:

* **Inicialização de modelos**: Instancia diferentes modelos de IA (Nova Pro, Claude Haiku, Claude Sonnet)
* **Aplicação de templates**: Utiliza PromptTemplate para estruturar prompts
* **Gerenciamento de tokens**: Implementa controle inteligente via `TokenManager`
* **Execução de inferência**: Processa requisições através do `BedrockInferenceService`

### 🤖 Modelos de IA Suportados

* **[Amazon Nova Pro](models/amazon_nova_pro.py)**: Modelo multimodal avançado da AWS
* **[Anthropic Claude Haiku](models/anthropic_claude_haiku.py)**: Modelo rápido e eficiente para tarefas simples
* **[Anthropic Claude Sonnet](models/anthropic_claude_sonnet.py)**: Modelo balanceado para tarefas complexas

### 📊 Gerenciamento de Tokens

O `TokenManager` implementa:
- **Contagem precisa** de tokens para otimização de custos
- **Controle de limites** para diferentes modelos
- **Batching inteligente** para prompts longos

## 🔀 Arquitetura da aplicação

O sistema segue uma arquitetura serverless modular:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Prompt Input  │───▶│  Lambda Handler  │───▶│  Model Classes  │
│   (Event Data)  │    │  (Orchestrator)  │    │ (Nova/Claude)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Response      │◀───│  Bedrock Service │◀───│  Prompt Template│
│   (AI Output)   │    │  (AWS Bedrock)   │    │   (Structured)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Estrutura do projeto

A estrutura do projeto é organizada da seguinte maneira:

```
AWSLambda-BedrockInference/
├── lambda_handler.py              # Orquestrador principal da Lambda
├── readme.md                      # Documentação do projeto
├── .env.example                   # Exemplo de variáveis de ambiente
├── .gitignore                     # Arquivos ignorados pelo Git
├── controllers/
│   └── token_manager.py           # Gerenciamento de tokens
├── models/
│   ├── amazon_nova_pro.py         # Modelo Amazon Nova Pro
│   ├── anthropic_claude_haiku.py  # Modelo Claude Haiku
│   └── anthropic_claude_sonnet.py # Modelo Claude Sonnet
├── services/
│   ├── bedrock_services.py        # Serviço principal do Bedrock
│   └── bedrock_inference.py       # Serviço de inferência
├── templates/
│   └── prompt_template.py         # Templates de prompts
├── tmp/                           # Arquivos temporários
└── utils/
    ├── check_aws.py               # Verificação de credenciais AWS
    └── import_credentials.py       # Importação de credenciais
```

## ⚙️ Configuração e variáveis de ambiente

O projeto utiliza as seguintes variáveis de ambiente:

```bash
# Credenciais AWS
AWS_ACCESS_KEY_ID="SUA_CHAVE_DE_ACESSO"
AWS_SECRET_ACCESS_KEY="SUA_CHAVE_SECRETA"
AWS_SESSION_TOKEN="SEU_TOKEN_DE_SESSÃO"

# Configuração do S3
S3_BUCKET_NAME="NOME_DO_BUCKET"

# IDs dos Modelos Bedrock
ANTHROPIC_CLAUDE_SONNET_MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
ANTHROPIC_CLAUDE_HAIKU_MODEL_ID="anthropic.claude-3-haiku-20240307-v1:0"
AMAZON_NOVA_PRO_MODEL_ID="amazon.nova-pro-v1:0"
```

Copie o arquivo .env.example para .env e configure suas credenciais.

## 📌 Como executar o projeto

Para executar o projeto localmente ou fazer deploy, siga as instruções abaixo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/rafael-torres-nantes/AWSLambda-BedrockInference.git
   cd AWSLambda-BedrockInference
   ```

2. **Configure as variáveis de ambiente:**
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   
   # Edite o arquivo .env com suas credenciais AWS
   nano .env  # Linux/Mac
   notepad .env  # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install boto3 python-dotenv
   ```

4. **Execute localmente para testes:**
   ```bash
   python lambda_handler.py
   ```

5. **Deploy na AWS Lambda:**
   - Comprima todos os arquivos em um arquivo ZIP
   - Faça upload na AWS Lambda Console
   - Configure as variáveis de ambiente no console da AWS
   - Ajuste timeout para pelo menos 5 minutos
   - Configure memória para 512MB ou superior

## 🎯 Funcionalidades de inferência

### Processamento Multi-Modelo
- **Múltiplos modelos**: Suporte simultâneo para Nova Pro, Claude Haiku e Sonnet
- **Seleção inteligente**: Escolha automática do modelo baseado no contexto
- **Fallback automático**: Alternativa entre modelos em caso de falha
- **Comparação de resultados**: Análise comparativa entre diferentes modelos

### Templates de Prompt Avançados
- **Templates estruturados**: Prompts padronizados para diferentes casos de uso
- **Contextualização dinâmica**: Adaptação automática ao domínio da consulta
- **Otimização de tokens**: Redução inteligente de tokens desnecessários
- **Formatação consistente**: Saídas padronizadas e bem estruturadas

### Monitoramento e Controle
- **Contagem de tokens**: Rastreamento preciso do uso de tokens
- **Logs detalhados**: Monitoramento completo do processo de inferência
- **Métricas de performance**: Análise de tempo de resposta e qualidade
- **Controle de custos**: Otimização automática para reduzir gastos

### Integração Serverless
- **Execução sob demanda**: Ativação apenas quando necessário
- **Escalabilidade automática**: Ajuste automático de recursos
- **Baixa latência**: Resposta rápida para consultas simples
- **Integração nativa**: Comunicação direta com outros serviços AWS

## 🕵️ Dificuldades Encontradas

Durante o desenvolvimento do projeto, algumas dificuldades foram enfrentadas, como:

- **Gerenciamento multi-modelo**: Cada modelo Bedrock possui formatos de requisição específicos, exigindo classes especializadas para cada um
- **Otimização de tokens**: Implementação de um sistema sofisticado de contagem e otimização de tokens para diferentes modelos com limites variados
- **Integração com credenciais**: Configuração segura de autenticação AWS em ambiente serverless com diferentes tipos de credenciais
- **Debugging serverless**: Implementação de logs detalhados para facilitar o debugging em ambiente distribuído da AWS Lambda
- **Templates de prompt**: Desenvolvimento de templates flexíveis que funcionem efetivamente com diferentes modelos de IA
- **Controle de custos**: Balanceamento entre qualidade das respostas e otimização de custos de uso dos modelos
- **Timeouts de Lambda**: Otimização do código para evitar timeouts em inferências mais complexas