import allure

from methods import authorize_user, create_order, generate_user_credentials, \
    get_all_orders, get_ingredients_hashes, get_orders, register_user


class TestGetOrders:

    @allure.title('Запрос заказов с авторизацией возвращает код 200 и набор заказов')
    def test_get_orders_with_auth(self):
        credentials = generate_user_credentials()
        register_user(credentials)
        auth_response = authorize_user(credentials)

        ingredients_hashes = get_ingredients_hashes()
        create_order(ingredients_hashes, {'Authorization': auth_response.json()['accessToken']})

        response = get_orders({'Authorization': auth_response.json()['accessToken']})
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'orders' in response.json()
        orders = response.json()['orders']
        for order in orders:
            assert '_id' in order
            assert 'status' in order
            assert 'number' in order
            assert 'createdAt' in order
            assert 'updatedAt' in order
            for ingredient_hash in order['ingredients']:
                assert ingredient_hash in ingredients_hashes
        assert 'total' in response.json()
        assert 'totalToday' in response.json()

    @allure.title('Запрос заказов с авторизацией возвращает код 401 и сообщение об ошибке')
    def test_get_orders_without_auth(self):
        response = get_orders()
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'You should be authorised'

    @allure.title('Запрос всех заказов без авторизации возвращает код 200 и набор заказов')
    def test_get_all_orders(self):
        response = get_all_orders()
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'orders' in response.json()
        orders = response.json()['orders']
        for order in orders:
            assert '_id' in order
            assert 'status' in order
            assert 'number' in order
            assert 'createdAt' in order
            assert 'updatedAt' in order
        assert 'total' in response.json()
