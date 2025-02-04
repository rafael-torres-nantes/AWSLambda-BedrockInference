# AWS Lambda - Bedrock Inference Project

## 👨‍💻 Projeto desenvolvido por: 
[Rafael Torres Nantes](https://github.com/rafael-torres-nantes)

## Índice

* [📚 Contextualização do projeto](#-contextualização-do-projeto)
* [🛠️ Tecnologias/Ferramentas utilizadas](#%EF%B8%8F-tecnologiasferramentas-utilizadas)
* [🖥️ Funcionamento do sistema](#%EF%B8%8F-funcionamento-do-sistema)
    * [🧩 Parte 1 - Backend](#parte-1---backend)
* [🔀 Arquitetura da aplicação](#arquitetura-da-aplicação)
* [📁 Estrutura do projeto](#estrutura-do-projeto)
* [📌 Como executar o projeto](#como-executar-o-projeto)
* [🕵️ Dificuldades Encontradas](#%EF%B8%8F-dificuldades-encontradas)

## 📚 Contextualização do projeto

O projeto tem como objetivo criar uma solução automatizada para gerar respostas a partir de prompts utilizando **AWS Bedrock**, uma plataforma de inteligência artificial generativa. O sistema foi desenhado para processar e analisar prompts, gerando respostas relevantes e precisas.

## 🛠️ Tecnologias/Ferramentas utilizadas

[<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/Visual_Studio_Code-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/bedrock/)
[<img src="https://img.shields.io/badge/Boto3-0073BB?logo=amazonaws&logoColor=white">](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[<img src="https://img.shields.io/badge/Dotenv-004400?logo=dotenv&logoColor=white">](https://pypi.org/project/python-dotenv/)

## 🖥️ Funcionamento do sistema

### 🧩 Parte 1 - Backend

O backend da aplicação foi desenvolvido utilizando **Python**. As principais funcionalidades incluem a integração com AWS Bedrock para a geração de respostas a partir de prompts.

* **Serviços AWS**: A integração com AWS Bedrock está localizada em `services/bedrock_inference.py`.
* **Utilitários**: A pasta `utils` contém funções para importação de credenciais AWS e outras funções auxiliares.

## 🔀 Arquitetura da aplicação

O sistema é baseado em uma arquitetura de microserviços, onde o backend se comunica com os serviços da AWS para análise e processamento dos prompts. O AWS Bedrock desempenha um papel central na geração das respostas.

## 📁 Estrutura do projeto

A estrutura do projeto é organizada da seguinte maneira:

```
.
├── services/
│   └── bedrock_inference.py
├── utils/
│   ├── check_aws.py
│   └── import_credentials.py
├── main.py
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## 📌 Como executar o projeto

Para executar o projeto localmente, siga as instruções abaixo:

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/aws-bedrock-inference.git
    ```

2. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure as variáveis de ambiente:**
    Renomeie o arquivo `.env.example` para `.env` e preencha com suas credenciais AWS.

4. **Execute o script principal:**
    ```bash
    python main.py
    ```

## 🕵️ Dificuldades Encontradas

Durante o desenvolvimento do projeto, algumas dificuldades foram enfrentadas, como:

- **Integração com serviços AWS:** O uso de credenciais e permissões para acessar o AWS Bedrock exigiu cuidados especiais para garantir a segurança e funcionalidade do sistema.
- **Aprimoramento do modelo de resposta:** O ajuste fino dos prompts e o treinamento de modelos gerativos para obter respostas mais precisas e relevantes foi um desafio contínuo.