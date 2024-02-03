import allure
import pytest
from methods import authorize_user, edit_user, generate_user_credentials, register_user


class TestEditUser:

    @allure.title('Успешное изменение пользовательских данных возвращает код 200 и сообщение об успехе')
    @pytest.mark.parametrize(
        "new_email,new_password,new_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_edit_authorized_user(self, new_email, new_password, new_name):
        credentials = generate_user_credentials()
        register_response = register_user(credentials)  # Регистрируем пользователя
        assert register_response.status_code == 200

        auth_response = authorize_user(credentials)  # Авторизуем пользователя
        assert auth_response.status_code == 200
        user = auth_response.json()['user']  # Получаем текущие данные

        # Меняем пользовательские данные
        new_credentials = generate_user_credentials()
        if new_email:
            user['email'] = new_credentials['email']
        if new_password:
            user['password'] = new_credentials['password']
        if new_name:
            user['name'] = new_credentials['name']

        edit_response = edit_user(user, {'Authorization': auth_response.json()['accessToken']})
        assert edit_response.status_code == 200
        assert edit_response.json()['success'] is True
        assert edit_response.json()['user']['email'] == user['email']
        assert edit_response.json()['user']['name'] == user['name']

    @allure.title('Изменение email на чужой существующий возвращает код 403 и сообщение об ошибке')
    def test_edit_authorized_used_with_used_email(self):
        credentials_1 = generate_user_credentials()
        register_response = register_user(credentials_1)  # Регистрируем пользователя #1
        assert register_response.status_code == 200

        credentials_2 = generate_user_credentials()
        register_response = register_user(credentials_2)  # Регистрируем пользователя #2
        assert register_response.status_code == 200

        auth_response = authorize_user(credentials_2)  # Авторизуем пользователя #2
        assert auth_response.status_code == 200
        user = auth_response.json()['user']  # Получаем текущие данные
        user['email'] = credentials_1['email']  # Меняем почту на почту пользователя #1

        edit_response = edit_user(user, {'Authorization': auth_response.json()['accessToken']})
        assert edit_response.status_code == 403
        assert edit_response.json()['message'] == 'User with such email already exists'

    @allure.title('Изменение пользовательских данных без авторизации возвращает код 401 и сообщение об ошибке')
    @pytest.mark.parametrize(
        "new_email,new_password,new_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_edit_not_authorized_user(self, new_email, new_password, new_name):
        credentials = generate_user_credentials()
        register_response = register_user(credentials)  # Регистрируем пользователя
        assert register_response.status_code == 200
        user = register_response.json()['user']

        # Меняем пользовательские данные
        new_credentials = generate_user_credentials()
        if new_email:
            user['email'] = new_credentials['email']
        if new_password:
            user['password'] = new_credentials['password']
        if new_name:
            user['name'] = new_credentials['name']

        edit_response = edit_user(user)
        assert edit_response.status_code == 401
        assert edit_response.json()['message'] == 'You should be authorised'
