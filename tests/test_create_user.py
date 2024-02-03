import allure
import pytest
from methods import generate_user_credentials, register_user


class TestCreateUser:

    @allure.title('Успешная регистрация уникального пользователя возвращает код 200 и сообщение от успехе')
    def test_create_unique_user(self):
        credentials = generate_user_credentials()
        response = register_user(credentials)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == credentials['email']
        assert response.json()['user']['name'] == credentials['name']
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()

    @allure.title('Регистрация прежде зарегистрированного пользователя возвращает код 403 и сообщение об ошибке')
    def test_create_already_existing_user(self):
        credentials = generate_user_credentials()
        response = register_user(credentials)
        assert response.status_code == 200
        response = register_user(credentials)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'

    @allure.title('Регистрация пользователя без обязательного поля возвращает код 403 и сообщение об ошибке')
    @pytest.mark.parametrize(
        "exclude_email,exclude_password,exclude_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_create_user_without_required_field(self, exclude_email, exclude_password, exclude_name):
        credentials = generate_user_credentials(exclude_email, exclude_password, exclude_name)
        response = register_user(credentials)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Email, password and name are required fields'
