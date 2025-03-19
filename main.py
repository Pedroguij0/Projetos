import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MISTRALAI_KEY") 
client = MistralClient(api_key=api_key)
history = []

def Send_Message(user_message):
    history.append(ChatMessage(role="user", content=user_message))
    response = client.chat(
        model="mistral-tiny",
        messages=history
    )
    resposta_bot = response.choices[0].message.content
    print("Bot:", resposta_bot)
    history.append(ChatMessage(role="assistant", content=resposta_bot))
print("Type 'exit' to quit.")
while True:
    user_input = input("Você: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Finishing chat, bye!")
        break
    elif user_input.lower() == "flw ai":
        print("Vlw ai bocó")
        break
    elif user_input.lower() == "sair":
        print("Encerrando a conversa, Adeus!")
        break
    Send_Message(user_input)
