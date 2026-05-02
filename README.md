# Consulting Platform

Платформа для автоматической генерации консалтинговых отчётов на основе мультиагентной системы Claude AI. Загружаете документы в базу знаний, описываете главы отчёта — агенты исследуют тему и пишут текст в реальном времени.

## Как работает

1. Создайте отчёт и добавьте главы
2. Загрузите документы (PDF, DOCX) в базу знаний отчёта
3. Настройте агентную команду для каждой главы: роли воркеров, промпты, количество раундов обсуждения
4. Запустите генерацию — наблюдайте за работой агентов в реальном времени через WebSocket

Генерация проходит в 4 шага:
- **Supervisor** создаёт план и распределяет задачи по воркерам
- **Workers** параллельно исследуют тему, опираясь на документы из базы знаний
- **Discussion rounds** — supervisor может запросить дополнительные исследования
- **Aggregation** — supervisor пишет финальный markdown (потоковый вывод)

## Стек

| Слой | Технологии |
|------|-----------|
| Frontend | Vue 3, TypeScript, Pinia, Vue Router |
| Backend | Python, FastAPI, SQLAlchemy (async), aiosqlite |
| AI | Anthropic Claude API (`claude-sonnet-4-6`) |
| Форматы документов | PyMuPDF (PDF), python-docx (DOCX) |
| Деплой | Docker, docker-compose, nginx |

## Быстрый старт

### Требования

- Docker и Docker Compose
- Anthropic API ключ

### Запуск

```bash
# 1. Скопируйте файл конфигурации
cp consulting-platform/backend/.env.example consulting-platform/backend/.env

# 2. Добавьте API ключ
echo "ANTHROPIC_API_KEY=sk-ant-..." >> consulting-platform/backend/.env

# 3. Запустите
cd consulting-platform
docker-compose up --build
```

Приложение доступно на `http://localhost`.  
API документация: `http://localhost:8000/docs`.

### Локальная разработка (без Docker)

**Backend:**
```bash
cd consulting-platform/backend
pip install -r requirements.txt
cp .env.example .env  # заполните ANTHROPIC_API_KEY
uvicorn main:app --reload
```

**Frontend:**
```bash
cd consulting-platform/frontend
npm install
npm run dev
```

## Конфигурация

Все настройки через переменные окружения в `backend/.env`:

| Переменная | По умолчанию | Описание |
|-----------|-------------|---------|
| `ANTHROPIC_API_KEY` | — | Ключ Anthropic API (обязательно) |
| `DEFAULT_MODEL` | `claude-sonnet-4-6` | Модель Claude для агентов |
| `DATABASE_URL` | SQLite в `./data/` | URL базы данных |
| `UPLOAD_DIR` | `./uploads` | Папка для загружаемых файлов |
| `MAX_UPLOAD_MB` | `50` | Максимальный размер файла |

## Структура проекта

```
consulting-platform/
├── backend/
│   ├── agents/             # Мультиагентная система
│   │   ├── orchestrator.py # Управление процессом генерации
│   │   ├── supervisor.py   # Агент-супервайзер (план, ревью, агрегация)
│   │   ├── worker.py       # Агент-воркер (исследование темы)
│   │   ├── message_bus.py  # In-process шина событий (asyncio.Queue)
│   │   ├── models.py       # Dataclass-модели агентов
│   │   └── prompts.py      # Системные промпты
│   ├── knowledge_base/
│   │   ├── extractor.py    # Извлечение текста из PDF/DOCX
│   │   ├── chunker.py      # Разбивка текста на чанки (200–800 символов)
│   │   └── store.py        # In-memory индекс с поиском по токенам
│   ├── routers/            # FastAPI роутеры
│   ├── models/             # SQLAlchemy ORM-модели
│   ├── schemas/            # Pydantic-схемы запросов/ответов
│   ├── core/               # Конфиг, БД, зависимости
│   └── main.py
├── frontend/
│   └── src/
│       ├── views/          # Страницы приложения
│       ├── components/     # UI-компоненты
│       ├── stores/         # Pinia-сторы
│       ├── api/            # HTTP-клиент для каждого роутера
│       └── composables/    # useWebSocket — стриминг прогресса генерации
└── docker-compose.yml
```

## API

Основные эндпоинты:

| Метод | URL | Описание |
|-------|-----|---------|
| `GET/POST` | `/reports` | Список и создание отчётов |
| `GET/POST` | `/reports/{id}/chapters` | Главы отчёта |
| `POST` | `/generation/runs` | Запуск генерации главы |
| `GET` | `/generation/runs/{id}` | Статус и результат генерации |
| `POST` | `/kb/{report_id}/documents` | Загрузка документа в базу знаний |
| `WS` | `/ws/runs/{run_id}` | Стриминг событий генерации |

Полная документация: `http://localhost:8000/docs`

## Данные

- База данных: SQLite (volume `sqlite_data`)
- Загруженные файлы: volume `kb_uploads`
- Чанки хранятся рядом с файлами как `.chunks.json` sidecar-файлы и перезагружаются при старте сервера
