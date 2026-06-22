# RoomSlot

RoomSlot — сервис для бронирования учебных комнат и переговорок в кампусе. Пользователь регистрируется, открывает страницу комнаты, выбирает свободный часовой слот в будний день, создаёт бронь, а другие пользователи видят изменение занятости в реальном времени через WebSocket.

## Архитектура

```text
Браузер
  -> Nginx HTTPS reverse proxy
      -> roomslot.local      -> Laravel SSR frontend (Blade + небольшой React-компонент)
      -> api.roomslot.local  -> FastAPI REST API + WebSocket
          -> MySQL
          -> Redis Pub/Sub
      <- WebSocket-обновления через Nginx
```

Распределение ответственности:

- **Nginx** принимает HTTPS-запросы, маршрутизирует Laravel и FastAPI по host и проксирует WebSocket.
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
- Nginx
- SQLAdmin

## Локальный запуск

Создать env-файлы:

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
```

Для Docker в `frontend/.env` должны быть такие значения: Laravel обращается к FastAPI по имени сервиса, а браузер — через Nginx-домен.

```env
FASTAPI_URL=http://api:8000
FASTAPI_BROWSER_URL=https://api.roomslot.local
FASTAPI_WS_URL=wss://api.roomslot.local
```

Добавить локальные домены в `/etc/hosts`:

```bash
sudo nano /etc/hosts
```

Добавить строки:

```text
127.0.0.1 roomslot.local
127.0.0.1 api.roomslot.local
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
https://roomslot.local
```

FastAPI через Nginx доступен по адресу:

```text
https://api.roomslot.local/health/live
```

Nginx генерирует self-signed сертификат внутри Docker image. При первом открытии браузер покажет предупреждение о небезопасном сертификате; для локального запуска нужно принять исключение для `roomslot.local` и `api.roomslot.local`.

## Админка

FastAPI подключает SQLAdmin по адресу:

```text
https://api.roomslot.local/admin
```

Данные администратора задаются через переменные окружения:

```env
BACKEND__ADMIN__USERNAME=admin
BACKEND__ADMIN__PASSWORD=admin123
BACKEND__ADMIN__SECRET_KEY=change-me-admin-secret-key
```

Через админку можно управлять комнатами, просматривать пользователей и просматривать бронирования. Создание и изменение бронирований через SQLAdmin отключены, чтобы не обходить доменные правила бронирования.

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
- Рабочее окно: 10:00-19:00 по Екатеринбургу.
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
- `GET /admin` — SQLAdmin

WebSocket endpoint:

- `GET /ws/rooms/{room_id}` через `wss://api.roomslot.local/ws/rooms/{room_id}`

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
nginx/     Nginx reverse proxy, HTTPS и WebSocket proxy
```
