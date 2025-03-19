from faker import Faker
import pytest
import logging
from api_client.api_client import APIClient
from settings import Settings as St




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def api_client():
    return APIClient(St.BASE_URL)

@pytest.fixture
def create_data_fake_user():
    """Метод для создания данных пользователя, возвращает словарь"""
    #Создаем фейковые данные заказчика
    fake = Faker("ru_RU")
    name = fake.first_name_female()
    password = fake.password()
    email = fake.email()

    payload = {"name": name,
                "password": password,
                "email": email
                }
    return payload

@pytest.fixture
def create_user(api_client, create_data_fake_user):
    #Регистрация пользователя
    payload = create_data_fake_user
    response_register = api_client.post(St.ENDPOINT_REGISTER, payload)
    # Проверяем статус код ответа при регистрации
    assert response_register.status_code == 200, f"Ожидался статус код 200, но получен {response_register.status_code}"
    # Получаем тело ответа в формате JSON
    response_data_register = response_register.json()
    # Извлекаем токен для удаления пользователя
    token_login = response_data_register["accessToken"]
    refresh_token = response_data_register["refreshToken"]
    yield {
        "payload": payload,
        "response_data_register": response_data_register,
        "token": token_login,
        "refresh_token": refresh_token
    }
    # Удаление пользователя после завершения теста
    headers = {"Authorization": token_login}
    response_delete = api_client.delete(St.ENDPOINT_DELETE_USER, headers=headers)
    # Проверяем статус код ответа при удалении
    assert response_delete.status_code == 202, \
        f"Ожидался статус код 202, но получен {response_delete.status_code}"


@pytest.fixture
def login_user(api_client, create_data_fake_user, create_user):
    data_create_user = create_user
    payload = data_create_user.get("payload")
    # Логин пользователя для получения токена
    response_login = api_client.post(St.ENDPOINT_LOGIN, payload)
    # Проверяем статус код ответа при логине
    assert response_login.status_code == 200, \
        f"Ожидался статус код 200, но получен {response_login.status_code}"
    # Получаем тело ответа в формате JSON
    response_data_login = response_login.json()
    # Извлекаем токен для удаления пользователя
    token_login = response_data_login["accessToken"]
    refresh_token = response_data_login["refreshToken"]
    # Передаем данные пользователя и токен в тест
    yield {
        "payload": payload,
        "response_data_login": response_data_login,
        "token": token_login,
        "refresh_token": refresh_token
    }



@pytest.fixture
def create_list_ingredients(api_client):
    """
    Фикстура для создания списков _id ингредиентов: булки, котлеты, соусы.
    """
    # Получаем список всех ингредиентов
    response = api_client.get(St.ENDPOINT_GET_INGREDIENTS)
    assert response.status_code == 200, f"Ожидался статус код 200, но получен {response.status_code}"

    # Получаем данные из ответа
    ingredients_data = response.json()["data"]

    # Разделяем ингредиенты на три списка и извлекаем _id
    buns = [ingredient["_id"] for ingredient in ingredients_data if ingredient["type"] == "bun"]
    mains = [ingredient["_id"] for ingredient in ingredients_data if ingredient["type"] == "main"]
    sauces = [ingredient["_id"] for ingredient in ingredients_data if ingredient["type"] == "sauce"]

    # Возвращаем три списка _id
    return {
        "buns": buns,
        "mains": mains,
        "sauces": sauces,
    }

@pytest.fixture
def create_user_orders(api_client, login_user, create_list_ingredients):
    """
    Фикстура для создания заказов пользователя.
    Возвращает данные для авторизации (токен) и список созданных заказов.
    """
    # Получаем данные пользователя и списки ингредиентов
    data_user = login_user
    list_ingredients = create_list_ingredients
    token_login = data_user.get("token")
    headers = {"Authorization": token_login}

    # Выбираем первый и последний элемент из каждого списка ингредиентов
    buns = list_ingredients["buns"]
    mains = list_ingredients["mains"]
    sauces = list_ingredients["sauces"]

    # Список для хранения созданных заказов
    created_orders = []

    # Создаем два заказа
    for ing in [0, -1]:  # Первый и последний ингредиенты
        payload = {"ingredients": [buns[ing], mains[ing], sauces[ing]]}

        # Отправляем запрос на создание заказа
        response = api_client.post(St.ENDPOINT_CREATE_ORDER, data=payload, headers=headers)

        # Проверяем статус код ответа
        assert response.status_code == 200, f"Ожидался статус код 200, но получен {response.status_code}"

        # Сохраняем данные созданного заказа
        order_data = response.json()
        created_orders.append(order_data)

    # Возвращаем данные для авторизации и список созданных заказов
    return {
        "headers": headers,
        "orders": created_orders,
    }
