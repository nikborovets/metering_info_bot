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

## Запуск через Docker

Сначала выполните сборку Docker-образа:

```bash
docker build --tag metering_info_bot .
```

Затем запустите контейнер:

```bash
docker run -it metering_info_bot
```