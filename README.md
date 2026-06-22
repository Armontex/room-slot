# RoomSlot

RoomSlot — сервис для бронирования учебных комнат и переговорок в кампусе. Пользователь регистрируется, открывает страницу комнаты, выбирает свободный часовой слот в будний день, создаёт бронь, а другие пользователи видят изменение занятости в реальном времени через WebSocket.

## Архитектура

```text
Браузер
  -> Laravel SSR frontend (Blade + небольшой React-компонент)
      -> FastAPI REST API
          -> MySQL
          -> Redis Pub/Sub
      <- WebSocket-обновления от FastAPI
```

Распределение ответственности:

- **Laravel** рендерит SSR-страницы, хранит access token FastAPI в server-side session и отправляет пользовательские действия в FastAPI.
- **FastAPI** отвечает за авторизацию, пользователей, комнаты, слоты, бронирования, запись в MySQL, публикацию событий в Redis, подписку на Redis и WebSocket-рассылку.
- **MySQL** хранит пользователей, комнаты и бронирования.
- **Redis** доставляет события бронирований в realtime-слой.
- **React** используется только на странице комнаты: компонент обновляет сетку слотов после WebSocket-событий.

## Стек

- Laravel 13
- FastAPI
- MySQL 8.4
- Redis 7
- React + Vite
- Docker Compose

## Локальный запуск

Создать env-файлы:

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
```

Для Docker в `frontend/.env` должны быть такие значения: Laravel обращается к FastAPI по имени сервиса, а браузер — через `localhost`.

```env
FASTAPI_URL=http://api:8000
FASTAPI_BROWSER_URL=http://localhost:8000
FASTAPI_WS_URL=ws://localhost:8000
```

Запустить сервисы:

```bash
docker compose up --build
```

В другом терминале применить миграции и создать тестовые комнаты:

```bash
make migrate
make seed-rooms
```

Открыть приложение:

```text
http://localhost:8080
```

FastAPI доступен по адресу:

```text
http://localhost:8000
```

## Основные сценарии

1. Зарегистрироваться.
2. Войти в аккаунт.
3. Открыть список комнат.
4. Открыть страницу одной комнаты.
5. Забронировать свободный часовой слот.
6. Открыть эту же комнату в другом окне браузера и проверить, что статус слота обновляется через WebSocket.
7. Открыть страницу "Мои бронирования" и отменить активную бронь.

## Правила бронирования

- Комнаты создаются заранее через seed-скрипт.
- Бронировать можно только будние дни.
- Слоты фиксированные, длительность каждого слота — 1 час.
- Рабочее окно: 10:00-19:00 по Екатеринбургу. Внутри backend слоты хранятся в UTC.
- На одну комбинацию `room_id + booking_date + slot_start` может существовать только одна активная бронь.
- Пользователь может отменить только свою бронь.

## База данных

Основные таблицы:

- `users` — зарегистрированные пользователи и хэши паролей.
- `rooms` — комнаты, доступные для бронирования.
- `bookings` — бронирования комнат на конкретную дату и часовой слот.

Связи:

- `bookings.user_id -> users.id`
- `bookings.room_id -> rooms.id`

Важные ограничения и индексы:

- generated column `active_slot_key` с unique constraint запрещает две активные брони на одну комнату, дату и слот;
- индекс для поиска бронирований по комнате, статусу, дате и времени;
- индекс для поиска бронирований пользователя.

## REST API

Реализованные эндпоинты:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `GET /rooms`
- `GET /rooms/{room_id}`
- `GET /rooms/{room_id}/slots`
- `POST /bookings`
- `POST /bookings/{booking_id}/cancel`
- `GET /me/bookings`
- `GET /health/live`
- `GET /health/ready`

WebSocket endpoint:

- `GET /ws/rooms/{room_id}`

## Realtime Flow

```text
Пользователь создаёт или отменяет бронь в Laravel
  -> Laravel отправляет запрос в FastAPI
  -> FastAPI валидирует действие и пишет изменение в MySQL
  -> FastAPI публикует событие бронирования в Redis
  -> Redis listener в FastAPI получает событие
  -> FastAPI отправляет событие WebSocket-клиентам этой комнаты
  -> React-компонент перезагружает сетку слотов
```

## Структура репозитория

```text
backend/   FastAPI-сервис, доменная логика, SQLAlchemy-модели, Alembic-миграции
frontend/  Laravel SSR frontend, Blade views, React-компонент слотов
knowledge_base/ материалы с требованиями и обсуждением проекта
```
