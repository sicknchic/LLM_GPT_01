import openai
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# API ket 설정
openai.api_key = os.getenv("OPENAI_API_KEY")


def custom_chatbot(user_message):
    prompt = "You're someone who shares kind and comforting words with people feeling tired or stressed."

    messages = [{"role": "system", "content": prompt}]

    messages.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    ai_response = response["choices"][0]["message"]["content"]

    return ai_response
