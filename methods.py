import allure
import random
import requests
import string


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
    return requests.post('https://stellarburgers.nomoreparties.site/api/auth/register', json=credentials)


@allure.step('Авторизуем пользователя')
def authorize_user(credentials) -> requests.Response:
    return requests.post('https://stellarburgers.nomoreparties.site/api/auth/login', json=credentials)


@allure.step('Обновляем данные пользователя')
def edit_user(user, headers=None) -> requests.Response:
    if headers:
        return requests.patch(
            'https://stellarburgers.nomoreparties.site/api/auth/user',
            user,
            headers=headers
        )
    else:
        return requests.patch(
            'https://stellarburgers.nomoreparties.site/api/auth/user',
            user
        )


@allure.step('Получаем список хэшей ингредиентов')
def get_ingredients_hashes() -> list:
    ingredients_response = requests.get('https://stellarburgers.nomoreparties.site/api/ingredients')
    return [ingredient['_id'] for ingredient in ingredients_response.json()['data']]


@allure.step('Создаём заказ')
def create_order(ingredients_hashes, headers=None) -> requests.Response:
    if headers:
        return requests.post(
            'https://stellarburgers.nomoreparties.site/api/orders',
            {'ingredients': ingredients_hashes},
            headers=headers
        )
    else:
        return requests.post(
            'https://stellarburgers.nomoreparties.site/api/orders',
            {'ingredients': ingredients_hashes}
        )


@allure.step('Получаем список заказов пользователя')
def get_orders(headers=None):
    if headers:
        return requests.get(
            'https://stellarburgers.nomoreparties.site/api/orders',
            headers=headers
        )
    else:
        return requests.get('https://stellarburgers.nomoreparties.site/api/orders')


@allure.step('Получаем список всех заказов')
def get_all_orders():
    return requests.get('https://stellarburgers.nomoreparties.site/api/orders/all')
