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

    chat_log = "chat_log.txt"

    with open(chat_log, "w", encoding="utf-8") as log_file:
        log_file.write("Chat Log:\n")
        log_file.write(f"prompt: {prompt}\n")
        log_file.write("-----" * 20 + "\n")

    while True:
        user_message = input("메세지를 입력해주세요. (종료: exit): ")

        if user_message.lower() == "exit":
            print("대화를 종료합니다.")
            break

        messages.append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

        ai_response = response["choices"][0]["message"]["content"]

        messages.append({"role": "assistant", "content": ai_response})

        with open(chat_log, "a", encoding="utf-8") as log_file:
            log_file.write(f"사용자: {user_message}\n")
            log_file.write(f"Chatbot: {ai_response}\n")
            log_file.write("-----" * 20 + "\n")

        print(f"system: {ai_response}")
