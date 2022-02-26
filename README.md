[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# Tourism Schedule Bot
Telegram-бот для студентов-бакалавров ИМОМИ ННГУ направления "Туризм". Бот выдает актуальное расписание на сегодня или завтра, 
а также может сказать, нижняя или верхняя сейчас неделя.

| Bot юзернейм               | Описание   |
| -------------------------- | ---------- |
| @tourism_schedule_bot      | Production |
| @tourism_schedule_stg_bot  | Staging    |

## Использование
Для работы требуется python>=3.9, зависимости, указанные в `requirements.txt` и _(опционально)_ Redis для хранения состояний. В переменных окружения 
нужно также выставить переменную `TOURISM_SCHEDULE_BOT_TOKEN=<your telegram bot token>`.
Если хотите использовать хранение состояний в Redis, то также нужно выставить переменную `REDIS_URL=<your redis connection url>`.
