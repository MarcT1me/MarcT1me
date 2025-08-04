# 💻 Backend Developer Portfolio

[Вернуться к главному портфолио](../README.md)

## ⚙️ Discord Bot с микросервисной архитектурой

![Статус](https://img.shields.io/badge/Active_development-0.0.1-blueviolet)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688?logo=fastapi&logoColor=white)
![DiscordAPI](https://img.shields.io/badge/Discord_API-2.3.2-5865F2?logo=discord&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0.7-2496ED?logo=docker&logoColor=white)
![PostgresSQL](https://img.shields.io/badge/PostgresSQL-13_alpine-4169E1?logo=postgresql&logoColor=white)

- хранение данных в PostgresSQL бд (отдельный Docker контейнер)
- авторизация через Discord
- отправка сообщения в канал Discord сервера по нажатию кнопки в клиенте

**Технологический стек**:

- Python 3.12 + FastAPI
- SQLAlchemy + PostgresSQL
- OAuth2 для авторизации через Discord
- Docker-контейнеризация

**Структура общения**

```mermaid
sequenceDiagram
    actor Client as Клиент
    participant Backend as Backand
    participant Bot as Discord-бот
    participant Database as База данных
    Note over Client, Bot: Клиентские запросы
    Client ->> Backend: HTTP Запрос (REST API)
    Backend ->> Database: SQL Запрос
    Database -->> Backend: Результаты запроса
    Backend -->> Client: JSON Ответ
    Note over Client, Bot: Команды бота
    Bot ->> Backend: Запрос /команда
    Backend ->> Database: Поиск данных
    Database -->> Backend: Данные пользователя
    Backend -->> Bot: Форматированный ответ
```

**GitHub**: [Исходный код](https://github.com/MarcT1me/GuardBotV2)

---

## ![Discord](https://img.shields.io/badge/-242429?logo=discord) простой Discord Bot

![Статус](https://img.shields.io/badge/Legacy-0.8.9-yellow)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![DiscordAPI](https://img.shields.io/badge/Discord_API-2.3.2-5865F2?logo=discord&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0.7-2496ED?logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)

- хранение данных в SQLite бд через Torties ORM
- команды voice каналов
- подключение к Google Console Cloud для авторизации в YouTube
- работа со сложными настройками через формы
- встроенная нейросеть Grok AI

**Технологический стек**:

- Python 3.12 + discord.py
- SQLite + Torties ORM
- OAuth2 для авторизации в Google (YouTube)
- OpenAI API для работы с Grok AI

**GitHub**: [Исходный код](https://github.com/MarcT1me/GuardBot)
