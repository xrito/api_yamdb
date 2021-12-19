# api_yamdb

## Примеры работы с авторизацией
### Запрос на отправку письма с кодом подтверждения

        curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth/signup/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "email": "test@test.com",
            "username": "test"
        }'
Если в БД не найдется пользователь с таким username - создастся новый пользователь
В результате выполнения метода отправляется код авторизации на почту пользователя. Посмотреть отправленные письма можно в папке sent_emails

### Запрос на авторизацию при помощи кода

        curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth/token/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "username": "test",
           "confirmation_code": "GQ0LM"
        }'

Если пользователь существует и код подтверждения верен, метод вернет AccessToken