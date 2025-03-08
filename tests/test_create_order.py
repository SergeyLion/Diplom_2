from settings import Settings as St
import pytest
import allure

@allure.feature("Тесты на создание заказов")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Тест проверяет создание заказа с авторизацией для первого и последнего ингредиента.")
    @pytest.mark.parametrize(
        "ing",
        [
            0,  # Первый из списка ингредиентов
            -1  # Последний из списка ингредиентов
        ],
        ids=[
            "First ingredient",
            "Last ingredient"
        ]
    )
    def test_create_order_with_authorization(self, api_client, login_user, create_list_ingredients, ing):
        with allure.step("Получаем данные пользователя и списки ингредиентов"):
            data_user = login_user
            list_ingredients = create_list_ingredients
            token_login = data_user.get("token")
            headers = {"Authorization": token_login}

        with allure.step("Выбираем ингредиенты для заказа"):
            buns = list_ingredients["buns"]
            mains = list_ingredients["mains"]
            sauces = list_ingredients["sauces"]

        with allure.step("Подготавливаем payload для создания заказа"):
            payload = {"ingredients": [buns[ing], mains[ing], sauces[ing]]}

        with allure.step("Отправляем запрос на создание заказа"):
            response = api_client.post(St.ENDPOINT_CREATE_ORDER, data=payload, headers=headers)

        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 200, f"Ожидался статус код 200, но получен {response.status_code}"

        with allure.step("Получаем тело ответа в формате JSON"):
            response_data = response.json()

        with allure.step("Проверяем, что ответ содержит ожидаемые поля"):
            assert "success" in response_data, "Поле 'success' отсутствует в ответе"
            assert "name" in response_data, "Поле 'name' отсутствует в ответе"
            assert "order" in response_data, "Поле 'order' отсутствует в ответе"

        with allure.step("Проверяем, что success равно True"):
            assert response_data["success"] is True, "Ожидалось 'success': True"

        with allure.step("Проверяем, что имя заказа не пустое"):
            assert response_data["name"], "Имя заказа пустое"

        with allure.step("Проверяем структуру и содержимое поля 'order'"):
            order_data = response_data["order"]
            assert "ingredients" in order_data, "Поле 'ingredients' отсутствует в 'order'"
            assert "_id" in order_data, "Поле '_id' отсутствует в 'order'"
            assert "owner" in order_data, "Поле 'owner' отсутствует в 'order'"
            assert "status" in order_data, "Поле 'status' отсутствует в 'order'"
            assert "createdAt" in order_data, "Поле 'createdAt' отсутствует в 'order'"
            assert "updatedAt" in order_data, "Поле 'updatedAt' отсутствует в 'order'"
            assert "number" in order_data, "Поле 'number' отсутствует в 'order'"
            assert "price" in order_data, "Поле 'price' отсутствует в 'order'"

        with allure.step("Проверяем, что список ингредиентов в заказе соответствует отправленным"):
            order_ingredients = order_data["ingredients"]
            assert len(order_ingredients) == 3, "Ожидалось 3 ингредиента в заказе"

        with allure.step("Проверяем, что ингредиенты в заказе соответствуют отправленным"):
            expected_ingredients = [buns[ing], mains[ing], sauces[ing]]
            for ingredient in order_ingredients:
                assert ingredient["_id"] in expected_ingredients, (
                    f"Ингредиент {ingredient['_id']} не соответствует ожидаемым"
                )

        with allure.step("Проверяем, что статус заказа 'done'"):
            assert order_data["status"] == "done", f"Ожидался статус 'done', но получен {order_data['status']}"

        with allure.step("Проверяем, что цена заказа корректная (сумма цен ингредиентов)"):
            expected_price = sum(ingredient["price"] for ingredient in order_ingredients)
            assert order_data["price"] == expected_price, (
                f"Ожидалась цена {expected_price}, но получена {order_data['price']}"
            )

    @allure.title("Создание заказа без авторизации")
    @allure.description("Тест проверяет создание заказа без авторизации для первого и последнего ингредиента.")
    @pytest.mark.parametrize(
        "ing",
        [
            0,  # Первый из списка ингредиентов
            -1  # Последний из списка ингредиентов
        ],
        ids=[
            "First ingredient",
            "Last ingredient"
        ]
    )
    def test_create_order_without_authorization(self, api_client, create_list_ingredients, ing):
        with allure.step("Получаем списки ингредиентов"):
            list_ingredients = create_list_ingredients

        with allure.step("Выбираем ингредиенты для заказа"):
            buns = list_ingredients["buns"]
            mains = list_ingredients["mains"]
            sauces = list_ingredients["sauces"]

        with allure.step("Подготавливаем payload для создания заказа"):
            payload = {"ingredients": [buns[ing], mains[ing], sauces[ing]]}

        with allure.step("Отправляем запрос на создание заказа"):
            response = api_client.post(St.ENDPOINT_CREATE_ORDER, data=payload)

        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 200, f"Ожидался статус код 200, но получен {response.status_code}"

        with allure.step("Получаем тело ответа в формате JSON"):
            response_data = response.json()

        with allure.step("Проверяем, что ответ содержит ожидаемые поля"):
            assert "success" in response_data, "Поле 'success' отсутствует в ответе"
            assert "name" in response_data, "Поле 'name' отсутствует в ответе"
            assert "order" in response_data, "Поле 'order' отсутствует в ответе"

        with allure.step("Проверяем, что success равно True"):
            assert response_data["success"] is True, "Ожидалось 'success': True"

        with allure.step("Проверяем, что имя заказа не пустое"):
            assert response_data["name"], "Имя заказа пустое"

        with allure.step("Проверяем структуру и содержимое поля 'order'"):
            order_data = response_data["order"]
            assert "number" in order_data, "Поле 'number' отсутствует в 'order'"

        with allure.step("Проверяем, что number целое число"):
            number = order_data["number"]
            assert isinstance(number, int), f"Значение для номера {number} должно быть целым числом"

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Тест проверяет создание заказа без ингредиентов.")
    def test_create_order_without_ingredients(self, api_client, login_user):
        with allure.step("Ожидаемое сообщение в ответе"):
            expected_message = "Ingredient ids must be provided"

        with allure.step("Получаем данные пользователя"):
            data_user = login_user
            token_login = data_user.get("token")
            headers = {"Authorization": token_login}

        with allure.step("Подготавливаем payload для создания заказа"):
            payload = {"ingredients": []}

        with allure.step("Отправляем запрос на создание заказа"):
            response = api_client.post(St.ENDPOINT_CREATE_ORDER, data=payload, headers=headers)

        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 400, f"Ожидался статус код 400, но получен {response.status_code}"

        with allure.step("Получаем тело ответа в формате JSON"):
            response_data = response.json()

        with allure.step("Проверяем, что ответ содержит ожидаемые поля"):
            assert "success" in response_data, "Поле 'success' отсутствует в ответе"
            assert "message" in response_data, "Поле 'message' отсутствует в ответе"

        with allure.step("Проверяем, что success равно False"):
            assert response_data["success"] is False, "Ожидалось 'success': False"

        with allure.step("Проверяем, что сообщение не пустое"):
            assert response_data["message"], "Сообщение пустое"

        with allure.step("Проверяем текст сообщения 'message'"):
            assert response_data["message"] == expected_message, (
                f"Ожидалось сообщение: {expected_message}, но получено: {response_data['message']}"
            )

    @allure.title("Создание заказа с неверным хешем ингредиента")
    @allure.description("Тест проверяет создание заказа с неверным хешем ингредиента.")
    def test_create_order_with_invalid_ingredient_hash(self, api_client, login_user):
        with allure.step("Получаем данные пользователя"):
            data_user = login_user
            token_login = data_user.get("token")
            headers = {"Authorization": token_login}

        with allure.step("Подготавливаем payload для создания заказа"):
            payload = {"ingredients": ["61c0c5a71d1f82001bdaaa", "61c0c5a71d1f82001bdaaa71", "61c0c5a71d1f82001bdaaa71"]}

        with allure.step("Отправляем запрос на создание заказа"):
            response = api_client.post(St.ENDPOINT_CREATE_ORDER, data=payload, headers=headers)

        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 500, f"Ожидался статус код 500, но получен {response.status_code}"