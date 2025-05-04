import os
import requests
from openai import OpenAI  # новый импорт

# Получаем токены из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_NAME = os.getenv("BOT_NAME", "Ваш бренд")

# Инициализация клиента OpenAI (новый формат!)
client = OpenAI(api_key=OPENAI_API_KEY)

# Генерация ответа с помощью ChatGPT
def generate_response(review_text, user_name):
    prompt = f"""
Ты — заботливый представитель бренда {BOT_NAME}. Напиши человечный, дружелюбный и уместный ответ на отзыв покупателя.

Отзыв: "{review_text}"
Имя: {user_name}

Ответь как живой человек, без шаблонов и сухости.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Ошибка OpenAI]: {e}")
        return "Ошибка генерации ответа."

# 🚀 Тестовый запуск без WB — просто проверка генерации
if __name__ == "__main__":
    review_text = "Костюм подошёл идеально, но ткань оказалась тоньше, чем ожидала."
    user_name = "Елена"
    response = generate_response(review_text, user_name)
    print(f"\nСгенерированный ответ для WB: {response}\n")
