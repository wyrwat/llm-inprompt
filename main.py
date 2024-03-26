import requests
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
AI_DEVS_KEY = os.getenv("AIDEVS_API_KEY")
TOKEN = "https://tasks.aidevs.pl/token/inprompt"
ANSWER = "https://tasks.aidevs.pl/answer"
TASK = "https://tasks.aidevs.pl/task"
TOKEN_PARAMS = {
    "apikey": AI_DEVS_KEY
}

token_response = requests.post(url=TOKEN, json=TOKEN_PARAMS)
token_response.raise_for_status()
token_data = token_response.json()
token = token_data["token"]

get_task_response = requests.get(url=f"{TASK}/{token}")
token_response.raise_for_status()
task_data = get_task_response.json()
task_input = task_data['input']
question = task_data['question']

chat = ChatOpenAI(api_key=OPEN_AI_KEY)
system_prompt = f"jakie imie wystepuje w podanym zdaniu. jako odpowiedź podaj tylko imie"
system_message = {"role": "system", "content": system_prompt}
human_message = HumanMessage(content=question)
response = chat.invoke([system_message, human_message])
name = response.content


def person_description():
    for text in task_input:
        if name in text:
            return text


person = person_description()
system_prompt = f"{person}"
system_message = {"role": "system", "content": system_prompt}
human_message = HumanMessage(content=question)
response = chat.invoke([system_message, human_message])
content = response.content

answer = {
    "answer": content
}
send_answer = requests.post(url=f"{ANSWER}/{token}", json=answer)
