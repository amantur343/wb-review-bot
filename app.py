import os
import requests
import time
import openai

# Получаем токены из переменных окружения
WB_API_KEY = os.getenv("WB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_NAME = os.getenv("BOT_NAME", "Ваш бренд")

openai.api_key = OPENAI_API_KEY

# Получение новых отзывов с Wildberries
def get_new_reviews():
    url = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
    headers = {
        "Authorization": WB_API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"[Ошибка получения отзывов]: {e}")
        return []

# Генерация ответа с помощью ChatGPT
def generate_response(review_text, user_name):
    prompt = f"""
Ты — заботливый представитель бренда {BOT_NAME}. Напиши человечный, дружелюбный и уместный ответ на отзыв покупателя.

Отзыв: "{review_text}"
Имя: {user_name}

Ответь как живой человек, без шаблонов и сухости.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[Ошибка OpenAI]: {e}")
        return "Спасибо за ваш отзыв! Мы обязательно учтём ваше мнение."

# Отправка ответа в Wildberries
def post_response(review_id, text):
    url = f"https://feedbacks-api.wildberries.ru/api/v1/feedbacks/{review_id}/response"
    headers = {
        "Authorization": WB_API_KEY,
        "Content-Type": "application/json"
    }
    json_data = {"text": text}
    try:
        response = requests.post(url, headers=headers, json=json_data)
        return response.status_code == 200
    except Exception as e:
        print(f"[Ошибка отправки ответа]: {e}")
        return False

# Главный цикл
def main_loop():
    while True:
        reviews = get_new_reviews()
        if not reviews:
            print("Нет новых отзывов или произошла ошибка.")
        for review in reviews:
            if not review.get("response"):
                user_name = review.get("userName", "Покупатель")
                text = review.get("text", "")
                review_id = review.get("id")
                response_text = generate_response(text, user_name)
                success = post_response(review_id, response_text)
                print(f"Ответ отправлен ({'успех' if success else 'ошибка'}): {response_text}")
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
