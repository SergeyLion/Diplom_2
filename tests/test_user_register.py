import allure
import pytest
from settings import Settings as St



@allure.feature("Тесты на регистрацию пользователя")
class TestUserRegister:

    @allure.title("Тест создания пользователя с уникальными данными")
    @allure.description("Тест проверяет успешное создание пользователя с валидными данными")
    def test_create_user_with_unique_credentials(self, api_client, create_user):
        with allure.step("Получаем данные пользователя из фикстуры"):
            data_user = create_user
            payload = data_user.get("payload")
            response_data = data_user.get("response_data_register")

        with allure.step("Проверяем, что ответ содержит ожидаемые поля"):
            assert "success" in response_data, "Поле 'success' отсутствует в ответе"
            assert "user" in response_data, "Поле 'user' отсутствует в ответе"
            assert "accessToken" in response_data, "Поле 'accessToken' отсутствует в ответе"
            assert "refreshToken" in response_data, "Поле 'refreshToken' отсутствует в ответе"

        with allure.step("Проверяем, что значение поля 'success' равно True"):
            assert response_data["success"] is True, f"Ожидалось 'success': True, но получено {response_data['success']}"

        with allure.step("Проверяем, что данные пользователя в ответе совпадают с отправленными данными"):
            user_data = response_data["user"]
            assert user_data["email"] == payload[
                "email"], f"Ожидался email: {payload['email']}, но получен {user_data['email']}"
            assert user_data["name"] == payload[
                "name"], f"Ожидалось имя: {payload['name']}, но получено {user_data['name']}"

        with allure.step("Проверяем, что accessToken и refreshToken не пустые"):
            assert response_data["accessToken"], "Поле 'accessToken' пустое"
            assert response_data["refreshToken"], "Поле 'refreshToken' пустое"

        with allure.step("Проверяем, что accessToken начинается с 'Bearer '"):
            assert response_data["accessToken"].startswith("Bearer "), "accessToken должен начинаться с 'Bearer '"

    @allure.title("Тест создания пользователя с уже существующими данными")
    @allure.description("Тест проверяет возврат ошибки при попытки создать пользователя с данными которые уже используются")
    def test_create_user_existing(self, api_client, create_user):
        with allure.step("Получаем данные пользователя из фикстуры"):
            data_user = create_user
            payload = data_user.get("payload")
            message_response = "User already exists"

        with allure.step("Повторное создание пользователя"):
            response_second = api_client.post(St.ENDPOINT_REGISTER, payload)

        with allure.step("Проверяем статус код ответа"):
            assert response_second.status_code == 403, f"Ожидался статус код 403, но получен {response_second.status_code}"

        with allure.step("Получаем тело ответа в формате JSON"):
            response_data = response_second.json()

        with allure.step("Проверяем, что ответ содержит ожидаемые поля"):
            assert "success" in response_data, "Поле 'success' отсутствует в ответе"
            assert "message" in response_data, "Поле 'message' отсутствует в ответе"

        with allure.step("Проверяем, что значение поля 'success' равно False"):
            assert response_data["success"] is False, \
                f"Ожидалось 'success': False, но получено {response_data['success']}"

        with allure.step("Проверяем, что значение поля 'message' соответствует ожидаемому"):
            assert response_data["message"] == message_response, \
                f"Ожидалось 'message': {message_response}, но получено {response_data['message']}"

    @pytest.mark.parametrize(
        "field",
        [
            "email",  # Удаляем email
            "name",   # Удаляем имени
            "password"  # Удаляем пароля
        ],
        ids=[
            "del_email",
            "del_name",
            "del_password"
        ]
    )
    @allure.title("Тест создания пользователя с отсутствующим обязательным полем")
    @allure.description(
        "Тест проверяет возврат ошибки, при отсутствие одного из обязательных полей при создание пользователя")
    def test_create_user_with_missing_required_field(self, api_client, create_data_fake_user, field):
        with allure.step("Подготавливаем данные для создания пользователя"):
            payload = create_data_fake_user
            message_response = "Email, password and name are required fields"

        with allure.step(f"Удаляем поле {field}"):
            del payload[field]

        with allure.step("Создаем пользователя"):
            response = api_client.post(St.ENDPOINT_REGISTER, payload)

        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 403, f"Ожидался статус код 403, но получен {response.status_code}"

        with allure.step("Получаем тело ответа в формате JSON"):
            response_data = response.json()

        with allure.step("Проверяем, что ответ содержит ожидаемые поля"):
            assert "success" in response_data, "Поле 'success' отсутствует в ответе"
            assert "message" in response_data, "Поле 'message' отсутствует в ответе"

        with allure.step("Проверяем, что значение поля 'success' равно False"):
            assert response_data["success"] is False, \
                f"Ожидалось 'success': False, но получено {response_data['success']}"

        with allure.step("Проверяем, что значение поля 'message' соответствует ожидаемому"):
            assert response_data["message"] == message_response, \
                f"Ожидалось 'message': {message_response}, но получено {response_data['message']}"