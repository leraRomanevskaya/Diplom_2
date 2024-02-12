import allure
import random
import requests
import string
from urls import URL_AUTH_LOGIN, URL_AUTH_REGISTER, URL_AUTH_USER, URL_INGREDIENTS, URL_ORDERS, URL_ORDERS_ALL


@allure.step('Генерируем учётные данные пользоваться')
def generate_user_credentials(exclude_email=False, exclude_password=False, exclude_name=False) -> dict:
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    credentials = {}

    if not exclude_email:
        credentials['email'] = generate_random_string(8) + '@ya.ru'

    if not exclude_password:
        credentials['password'] = generate_random_string(12)

    if not exclude_name:
        credentials['name'] = generate_random_string(8)

    return credentials


@allure.step('Регистрируем пользователя')
def register_user(credentials) -> requests.Response:
    return requests.post(URL_AUTH_REGISTER, json=credentials)


@allure.step('Авторизуем пользователя')
def authorize_user(credentials) -> requests.Response:
    return requests.post(URL_AUTH_LOGIN, json=credentials)


@allure.step('Обновляем данные пользователя')
def edit_user(user, headers=None) -> requests.Response:
    if headers:
        return requests.patch(URL_AUTH_USER, user, headers=headers)
    else:
        return requests.patch(URL_AUTH_USER, user)


@allure.step('Получаем список хэшей ингредиентов')
def get_ingredients_hashes() -> list:
    ingredients_response = requests.get(URL_INGREDIENTS)
    return [ingredient['_id'] for ingredient in ingredients_response.json()['data']]


@allure.step('Создаём заказ')
def create_order(ingredients_hashes, headers=None) -> requests.Response:
    if headers:
        return requests.post(URL_ORDERS, {'ingredients': ingredients_hashes}, headers=headers)
    else:
        return requests.post(URL_ORDERS, {'ingredients': ingredients_hashes})


@allure.step('Получаем список заказов пользователя')
def get_orders(headers=None):
    if headers:
        return requests.get(URL_ORDERS, headers=headers)
    else:
        return requests.get(URL_ORDERS)


@allure.step('Получаем список всех заказов')
def get_all_orders():
    return requests.get(URL_ORDERS_ALL)
