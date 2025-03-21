# Diplom_2

## Описание
Этот проект представляет собой набор тестов для API Stellar Burgers:
Проект содержит тесты для:
- Создание пользователя 
- Логин пользователя 
- Изменение данных пользователя
- Создание заказа
- Получение заказов конкретного пользователя

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:SergeyLion/Diplom_2.git
   
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt

3. Запустить тесты
   ```bash
   pytest tests/
   
4. Собрать отчет в allure:
   ```bash
   pytest .\tests --alluredir=allure_results
   
5. Открыть отчет allure:
   ```bash
   allure serve allure_results