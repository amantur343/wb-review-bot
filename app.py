import os
import requests
import time
import openai

WB_API_KEY = os.getenv("WB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_NAME = os.getenv("BOT_NAME", "Ваш бренд")

openai.api_key = OPENAI_API_KEY

def get_new_reviews():
    url = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
    headers = {
        "Authorization": WB_API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json().get("data", [])

def generate_response(review_text, user_name):
    prompt = f"""
Ты — заботливый представитель бренда {BOT_NAME}. Напиши человечный, дружелюбный и уместный ответ на отзыв:
Отзыв: "{review_text}"
Имя: {user_name}
Ответи как живой человек, не шаблонно.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def post_response(review_id, text):
    url = f"https://feedbacks-api.wildberries.ru/api/v1/feedbacks/{review_id}/response"
    headers = {
        "Authorization": WB_API_KEY,
        "Content-Type": "application/json"
    }
    json_data = {"text": text}
    response = requests.post(url, headers=headers, json=json_data)
    return response.status_code == 200

def main_loop():
    while True:
        reviews = get_new_reviews()
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