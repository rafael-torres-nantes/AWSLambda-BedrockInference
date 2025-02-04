from services.bedrock_inference import BedrockInference

bedrock_service = BedrockInference()

response = bedrock_service.invoke_model('bom dia, qual é seu nome?')
print(response)

questions = [
    "What is your favorite color?",
    "What is your favorite food?",
    "What is your favorite movie?",
    "What is your favorite book?",
    "What is your favorite hobby?",
    "What is your favorite sport?",
    "What is your favorite animal?",
    "What is your favorite season?",
    "What is your favorite holiday?",
    "What is your favorite song?",
    "What is your favorite TV show?",
    "What is your favorite game?",
    "What is your favorite subject in school?",
    "What is your favorite place to visit?",
    "What is your favorite type of music?"
]

for question in questions:
    response = bedrock_service.invoke_model(question)
    print(f"Question: {question}\nResponse: {response}\n")
    import time 
    time.sleep(1)