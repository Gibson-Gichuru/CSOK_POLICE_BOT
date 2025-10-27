# AI-Powered Discord Moderation Bot

This project is a **Discord moderation bot** powered by **OpenAI's GPT model**. The project was created initially with the intention of using it to moderate the [CSOK (Computer Society of Kimathi) discord server](https://discord.gg/YfhX6Znu).
It automatically classifies and removes messages that violate community guidelines — such as offensive, sexual, or self-promotional content — while allowing neutral, respectful discussions to thrive.

The bot also includes a fun feature that generates quirky welcome messages for new members using OpenAI's text generation models.

---

## Features

- **AI-Powered Moderation** — Uses GPT-4 to classify messages in real time.
- **Automatic Message Deletion** — Deletes posts that break community rules.
- **Personalized Welcome Messages** — Welcomes new members with AI-generated greetings.
- **Health Check Endpoint** — Exposes a simple Flask route (`/`) for deployment readiness checks.
- **Environment-Based Configuration** — Keeps tokens and API keys secure via `.env` file.

---

## How It Works

1. Every new message posted in a Discord server is sent to OpenAI’s GPT model.
2. The model classifies the message into one of:
   - `offensive`
   - `sexual`
   - `neutral`
   - `self-promotion`
3. If the message is not `neutral`, it is deleted, and the user is notified.
4. When a new member joins, a welcome message is generated using OpenAI’s text completion API.

---

## Project Structure

|--- apprunner.yml

|--- bot.py

|--- requirements.txt

|--- .env (Create your own)

|--- README.md

---



## How To Run It Locally

Create a .env file on the project's root folder and include the following variables:

```
open_ai_key=XXXXXXXXXXXXXXXXXXXXXXXX
```

```
discord_token=XXXXXXXXXXXXXXXXXXXXXXX
```

Run the following commands:

Create a virtual environment to run the script in an isolated environment

```
python3 -m venv venv
```

Activate the virtual environment you just created

```
source venv/bin/activate
```

Install packages

```
pip install -r requirements.txt
```

Run the script

```
	python3 bot.py
```
