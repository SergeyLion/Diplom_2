import allure
from settings import Settings as St
import pytest
from faker import Faker



@allure.feature("Тесты на обновление данных пользователя")
class TestUpdateUser:
    fake = Faker("ru_RU")
    name = fake.first_name_female()
    password = fake.password()
    email = fake.email()

    @pytest.mark.parametrize(
        "field, new_value",
        [
            ("email", email),  # Изменение email
            ("name", name),  # Изменение имени
            ("password", password)  # Изменение пароля
        ],
        ids=[
            "change_email",
            "change_name",
            "change_password"
        ]
    )
    @allure.title("Тест изменения данных пользователя с авторизацией")
    @allure.description("Тест проверяет успешный обновление данных пользователя авторизированного")
    def test_update_user_info_with_authorization(self, api_client, login_user, field, new_value):
        """
        Тест проверяет изменение данных пользователя:
        - Изменение email, имени и пароля для авторизованного пользователя.
        """
        with allure.step("Получаем данные пользователя из фикстуры"):
            data_user = login_user
            token_login = data_user.get("token")
            headers = {"Authorization": token_login}

        with allure.step("Подготавливаем данные для обновления"):
            update_payload = {field: new_value}

        with allure.step("Выполняем запрос на обновление данных"):
            response = api_client.patch(St.ENDPOINT_UPDATE_USER_INFO, data=update_payload, headers=headers)

        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 200, (
                f"Ожидался статус код 200, но получен {response.status_code}"
            )

        with allure.step("Проверяем тело ответа"):
            response_data = response.json()

        with allure.step("Проверяем, что success равно True"):
            assert response_data["success"] is True, "Ожидалось 'success': True"

        with allure.step("Проверяем, что данные пользователя обновились"):
            if field in ["email", "name"]:  # Пароль не возвращается в ответе
                assert response_data["user"][field] == new_value, (
                    f"Ожидалось, что поле {field} будет равно {new_value}, но получено {response_data['user'][field]}"
                )

    @pytest.mark.parametrize(
        "field, new_value",
        [
            ("email", email),  # Изменение email
            ("name", name),  # Изменение имени
            ("password", password)  # Изменение пароля
        ],
        ids=[
            "change_email",
            "change_name",
            "change_password"
        ]
    )
    @allure.title("Тест изменения данных пользователя без авторизации")
    @allure.description("Тест проверяет возврат ошибки при обновление данных пользователя без авторизации")
    def test_update_user_info_without_authorization(self, api_client, field, new_value):
        """
        Тест проверяет, что неавторизованный пользователь не может изменить данные.
        """
        with allure.step("Ожидаемое сообщение в ответе"):
            expected_message = "You should be authorised"

        with allure.step("Подготавливаем данные для обновления"):
            update_payload = {field: new_value}

        with allure.step("Выполняем запрос на обновление данных"):
            response = api_client.patch(St.ENDPOINT_UPDATE_USER_INFO, data=update_payload)

        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 401, "Ожидался статус код 401 для неавторизованного пользователя"

        with allure.step("Проверяем тело ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Ожидалось 'success': False"
            assert response_data["message"] == expected_message, (
                f"Ожидалось сообщение: {expected_message}, но получено: {response_data['message']}"
            )