import allure

from methods import authorize_user, create_order, generate_user_credentials, get_ingredients_hashes, register_user


class TestCreateOrder:

    @allure.title('Создание авторизованного заказа с ингредиентами возвращает код 200 и сообщение об успехе')
    def test_create_order_with_ingredients_with_auth(self):
        credentials = generate_user_credentials()
        register_response = register_user(credentials)  # Регистрируем пользователя
        assert register_response.status_code == 200

        auth_response = authorize_user(credentials)  # Авторизуем пользователя
        assert auth_response.status_code == 200

        ingredients_hashes = get_ingredients_hashes()

        response = create_order(ingredients_hashes, {'Authorization': auth_response.json()['accessToken']})
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'name' in response.json()
        assert 'order' in response.json()
        assert 'number' in response.json()['order']
        assert 'ingredients' in response.json()['order']
        hashes = [ingredient['_id'] for ingredient in response.json()['order']['ingredients']]
        for ingredient_hash in ingredients_hashes:
            assert ingredient_hash in hashes

    @allure.title('Создание авторизованного заказа без ингредиентов возвращает код 400 и сообщение об ошибке')
    def test_create_order_without_ingredients_with_auth(self):
        credentials = generate_user_credentials()
        register_response = register_user(credentials)  # Регистрируем пользователя
        assert register_response.status_code == 200

        auth_response = authorize_user(credentials)  # Авторизуем пользователя
        assert auth_response.status_code == 200

        response = create_order([], {'Authorization': auth_response.json()['accessToken']})
        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание авторизованного заказа с несуществующими ингредиентами возвращает код 500')
    def test_create_order_with_invalid_ingredients_hash_with_auth(self):
        credentials = generate_user_credentials()
        register_response = register_user(credentials)  # Регистрируем пользователя
        assert register_response.status_code == 200

        auth_response = authorize_user(credentials)  # Авторизуем пользователя
        assert auth_response.status_code == 200

        ingredients_hashes = ['this-is-invalid-hash']

        response = create_order(ingredients_hashes, {'Authorization': auth_response.json()['accessToken']})
        assert response.status_code == 500

    @allure.title('Создание не авторизованного заказа с ингредиентами возвращает код 200 и номер заказа')
    def test_create_order_with_ingredients_without_auth(self):
        ingredients_hashes = get_ingredients_hashes()

        response = create_order(ingredients_hashes)
        print(response.status_code)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'name' in response.json()
        assert 'order' in response.json()
        assert 'number' in response.json()['order']

    @allure.title('Создание не авторизованного заказа без ингредиентов возвращает код 400 и сообщение об ошибке')
    def test_create_order_without_ingredients_without_auth(self):
        response = create_order([])
        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание не авторизованного заказа с несуществующими ингредиентами возвращает код 500')
    def test_create_order_with_invalid_ingredients_hash_without_auth(self):
        ingredients_hashes = ['this-is-invalid-hash']

        response = create_order(ingredients_hashes)
        assert response.status_code == 500
