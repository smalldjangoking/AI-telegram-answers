<div align="center">

# AITelegramAnswers

A **Telegram bot powered by OpenAI** — satirical personas, conversation context, and chat protection via middleware.

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-2.x-60A5FA.svg)](https://python-poetry.org/)
[![Aiogram](https://img.shields.io/badge/aiogram-3.x-26A5E4.svg)](https://docs.aiogram.dev/)

</div>

---

## Overview

The bot replies in a **single allowed chat** when it is mentioned or when users reply to its messages. Answers are generated with **OpenAI Chat Completions** using a system prompt with a **daily persona** and **time-of-day** context. Each request includes the user’s **recent message history** and optional **context** (a quoted message or the bot’s previous reply).

> Replies follow **dark humor and satire** in a fixed tone. Use this only where it is appropriate and everyone in the chat agrees.

---

## Features

| Area | Details |
|------|---------|
| **Integration** | [Aiogram 3](https://docs.aiogram.dev/), async polling |
| **Model** | Configurable via `OPENAI_MODEL` (default `gpt-4o-mini`) |
| **Reliability** | Retries on timeouts and 5xx errors ([tenacity](https://github.com/jd/tenacity)) |
| **Config** | [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) + `.env` |
| **Guards** | Only chat `ALLOWED_CHAT_ID`, message length checks, text cleanup |

---

## Requirements

- **Python** 3.12–3.14
- **[Poetry](https://python-poetry.org/docs/#installation)** 2.x

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/AITelegramAnswers.git
cd AITelegramAnswers
poetry install
```

Create a `.env` file in the repository root (see the table below).

---

## Environment variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `BOT_USERNAME` | Bot username **without** `@` — used to detect mentions |
| `OPENAI_API_KEY` | [OpenAI](https://platform.openai.com/) API key |
| `ALLOWED_CHAT_ID` | Chat ID (group or supergroup) where the bot may respond |
| `OPENAI_MODEL` | *(optional)* Chat model; default `gpt-4o-mini` |
| `MAX_MESSAGE_LENGTH` | *(optional)* Max incoming text length (default `4000`) |

To get `chat_id`, forward a message from the target chat to a bot like [@userinfobot](https://t.me/userinfobot) or log it from your own code.

---

## Running

From the project root:

```bash
poetry run python -m bot.main
```

Or activate the Poetry environment and run `python -m bot.main` as usual.

---

## How to trigger the bot

1. **Mention** — a message that includes `@bot_username` (same as `BOT_USERNAME`).
2. **Reply to the bot** — use Telegram’s reply thread on the bot’s message (separate handler with stronger “waiting” copy).

While the API request is in flight, the bot edits a temporary “Thinking…” line with a random suffix from the project constants.

---

## Repository layout

```
bot/
├── main.py                 # Entry: Bot, Dispatcher, middleware, polling
├── core/
│   ├── config.py           # Environment-backed settings
│   └── constants.py        # “Waiting” lines for replies
├── handlers/
│   └── common_router.py    # Mention and reply-to-bot handlers
├── middleware/             # Chat allowlist, length, history, text
├── services/
│   ├── openai_service.py   # OpenAI client + retries
│   └── base_prompt_service.py  # System prompt and personas
└── helpers/
```

---

<div align="center">

Built for chats that want a **snarky AI commentator**, not a corporate assistant.

</div>
