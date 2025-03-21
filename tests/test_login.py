import pytest
from settings import Settings as St
import allure



@allure.feature("Тесты на авторизацию пользователя")
class TestLogin:

    @allure.title("Логин с валидными учетными данными")
    @allure.description("Тест проверяет успешный вход с валидными учетными данными.")
    def test_login_with_valid_credentials(self, api_client, create_user):
        with allure.step("Получаем данные зарегистрированного пользователя"):
            data_user = create_user
            payload = data_user.get("payload")

        with allure.step("Логинимся под созданным пользователем"):
            response_login = api_client.post(St.ENDPOINT_LOGIN, payload)

        with allure.step("Проверяем статус код ответа при логине"):
            assert response_login.status_code == 200, f"Ожидался статус код 200, но получен {response_login.status_code}"

        with allure.step("Получаем тело ответа в формате JSON"):
            response_data = response_login.json()

        with allure.step("Проверяем, что ответ содержит ожидаемые поля"):
            assert "success" in response_data, "Поле 'success' отсутствует в ответе"
            assert "accessToken" in response_data, "Поле 'accessToken' отсутствует в ответе"
            assert "refreshToken" in response_data, "Поле 'refreshToken' отсутствует в ответе"
            assert "user" in response_data, "Поле 'user' отсутствует в ответе"

        with allure.step("Проверяем, что значение поля 'success' равно True"):
            assert response_data["success"] is True, f"Ожидалось 'success': True, но получено {response_data['success']}"

        with allure.step("Проверяем, что данные пользователя в ответе совпадают с отправленными данными"):
            user_data = response_data["user"]
            assert user_data["email"] == payload["email"], (
                f"Ожидался email: {payload['email']}, но получен {user_data['email']}"
            )
            assert user_data["name"] == payload["name"], (
                f"Ожидалось имя: {payload['name']}, но получено {user_data['name']}"
            )

        with allure.step("Проверяем, что accessToken и refreshToken не пустые"):
            assert response_data["accessToken"], "Поле 'accessToken' пустое"
            assert response_data["refreshToken"], "Поле 'refreshToken' пустое"

        with allure.step("Проверяем, что accessToken начинается с 'Bearer '"):
            assert response_data["accessToken"].startswith("Bearer "), "accessToken должен начинаться с 'Bearer '"

    @allure.title("Логин с невалидными учетными данными")
    @allure.description("Тест проверяет логин с невалидными учетными данными: неверный email, пароль или оба.")
    @pytest.mark.parametrize(
        "email, password, description",
        [
            # Неверный пароль
            (None, "wrong_password", "Неверный пароль"),
            # Неверный email
            ("wrong_email@example.com", None, "Неверный email"),
            # Неверный email и пароль
            ("wrong_email@example.com", "wrong_password", "Неверный email и пароль"),
        ],
        ids=[
            "invalid_password",
            "invalid_email",
            "invalid_email_and_password",
        ]
    )
    def test_login_with_invalid_credentials(self, api_client, create_user, email, password, description):
        with allure.step("Ожидаемое сообщение в ответе"):
            message_response = "email or password are incorrect"

        with allure.step("Получаем данные зарегистрированного пользователя"):
            data_user = create_user
            payload = data_user.get("payload")

        with allure.step("Подготавливаем данные для логина"):
            login_payload = {
                "email": email if email is not None else payload["email"],  # Используем переданный email или оригинальный
                "password": password if password is not None else payload["password"],  # Используем переданный пароль или оригинальный
            }

        with allure.step("Логинимся с неверными учетными данными"):
            response_login = api_client.post(St.ENDPOINT_LOGIN, login_payload)

        with allure.step("Проверяем статус код ответа при логине"):
            assert response_login.status_code == 401, f"Ожидался статус код 401, но получен {response_login.status_code}"

        with allure.step("Получаем тело ответа в формате JSON"):
            response_data = response_login.json()

        with allure.step("Проверяем, что ответ содержит ожидаемые поля"):
            assert "success" in response_data, "Поле 'success' отсутствует в ответе"
            assert "message" in response_data, "Поле 'message' отсутствует в ответе"

        with allure.step("Проверяем, что значение поля 'success' равно False"):
            assert response_data["success"] is False, f"Ожидалось 'success': False, но получено {response_data['success']}"

        with allure.step("Проверяем, что сообщение об ошибке корректное"):
            assert response_data["message"] == message_response, (
                f"Ожидалось сообщение: {message_response}, но получено: {response_data['message']}"
            )