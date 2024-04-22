# Инструкции по запуску

## Шаг 1: Создание виртуального окружения

```bash
python3 -m venv venv
```

## Шаг 2: Активация виртуального окружения

### Для Linux/Mac:

```bash
source venv/bin/activate
```

### Для Windows:

```bash
venv\Scripts\activate
```

## Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 4: Запуск приложения

```bash
python3 main.py
```

## Запуск через Docker Compose

Сначала выполните сборку Docker-образа и запустите контейнер:

```bash
docker-compose up --build -d
```

## Запуск через Docker

Сначала выполните сборку Docker-образа:

```bash
docker build --tag metering_info_bot .
```

Затем запустите контейнер:

```bash
docker run -it metering_info_bot
```

## Изменение персональных данных

### Изменение .env файла

```bash
TOKEN=token
SPREADSHEET_ID=spreadsheet_id
GOOGLESHEETS_LINK=googlesheets_link
AUTHORIZED_USERS=userid1,userid2,userid3,userid4
```

### Создание creds.json

```bash
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "...",
  "universe_domain": "googleapis.com"
}

```
