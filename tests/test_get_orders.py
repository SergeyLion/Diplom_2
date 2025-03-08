from settings import Settings as St



class TestGetOrders:

    def test_get_user_orders_with_authorization(self, api_client, create_user_orders):
        # Получаем данные из фикстуры
        user_data = create_user_orders
        headers = user_data["headers"]  # Хедер для авторизации
        created_orders = user_data["orders"]

        # Отправляем запрос на получение заказов пользователя
        response = api_client.get(St.ENDPOINT_GET_USER_ORDERS, headers=headers)

        # Проверяем статус код ответа
        assert response.status_code == 200, f"Ожидался статус код 200, но получен {response.status_code}"

        # Получаем тело ответа в формате JSON
        response_data = response.json()

        # Проверяем, что ответ содержит ожидаемые поля
        assert "success" in response_data, "Поле 'success' отсутствует в ответе"
        assert "orders" in response_data, "Поле 'orders' отсутствует в ответе"
        assert "total" in response_data, "Поле 'total' отсутствует в ответе"
        assert "totalToday" in response_data, "Поле 'totalToday' отсутствует в ответе"

        # Проверяем, что success равно True
        assert response_data["success"] is True, "Ожидалось 'success': True"

        # Проверяем, что список заказов не пустой
        assert len(response_data["orders"]) == len(created_orders), "Количество заказов созданных и полученных не совпала"

        # Проверяем, что созданные заказы присутствуют в ответе
        for created_order in created_orders:
            created_order_id = created_order["order"]["_id"]
            found = False
            for order in response_data["orders"]:
                if order["_id"] == created_order_id:
                    found = True
                    # Проверяем, что данные заказа совпадают
                    ingredient_ids = []
                    for created_order_ingredients in created_order["order"]["ingredients"]:
                        ingredient_ids.append(created_order_ingredients["_id"])
                    assert order["ingredients"] == ingredient_ids, (
                        f"Ингредиенты заказа {created_order_id} не совпадают"
                    )
                    assert order["status"] == created_order["order"]["status"], f"Статус заказа {created_order_id} не совпадают"
                    assert order["name"] == created_order["name"], (
                        f"Имя заказа {created_order_id} не совпадает"
                    )
                    break
            assert found, f"Заказ {created_order_id} отсутствует в списке заказов пользователя"

        # Проверяем, что total и totalToday корректны
        assert isinstance(response_data["total"], int), "Поле 'total' должно быть целым числом"
        assert isinstance(response_data["totalToday"], int), "Поле 'totalToday' должно быть целым числом"
        assert response_data["total"] >= len(response_data["orders"]), (
            "Общее количество заказов меньше, чем количество заказов в ответе"
        )




    def test_get_user_orders_without_authorization(self,api_client):
        """
        Тест проверяет, что неавторизованный пользователь не может получить список заказов.
        """
        # Ожидаемое сообщение в ответе
        expected_message = "You should be authorised"

        # Выполняем запрос на обновление данных
        response = api_client.get(St.ENDPOINT_GET_USER_ORDERS)

        # Проверяем статус код ответа
        assert response.status_code == 401, "Ожидался статус код 401 для неавторизованного пользователя"

        # Проверяем тело ответа
        response_data = response.json()
        assert response_data["success"] is False, "Ожидалось 'success': False"
        assert response_data["message"] == expected_message, (
            f"Ожидалось сообщение: {expected_message}, но получено: {response_data['message']}"
        )


