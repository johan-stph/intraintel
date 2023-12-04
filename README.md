# IntraIntel Bot Documentation

This document provides instructions on how to build and run the IntraIntel bot using Docker.

## Prerequisites

- Docker installed on your machine. You can download and install Docker from [https://www.docker.com/](https://www.docker.com/).

## Build the Docker Image

To build the Docker image for the IntraIntel bot, execute the following command in the terminal:

```bash
sudo docker build -t intraintel .
```

This command builds the Docker image named `intraintel` from the current directory.

## Run the Docker Container

Once the Docker image is built, you can run the IntraIntel bot in a Docker container using the following command:

```bash
sudo docker run -d --rm --name intraintel -e DISCORD_API_KEY="your_discord_api_key" -e OPENAI_API_KEY="your_openai_api_key" intraintel:latest
```
This command starts the IntraIntel bot in detached mode within a Docker container.

A tutorial on how to set up your own discord bot and get a token for it can be found here: https://realpython.com/how-to-make-a-discord-bot-python/#creating-an-application <br>
Follow the steps in the section "How to Make a Discord Bot in the Developer Portal". <br>
When creating the bot make sure to enable "Bot > Privileged Gateway > Intents > Message Content Intent".
When generating the invite Link for the bot, under "OAuth2 > URL Generator" check "bot" in the section "Scopes" and "Administrator" under "Bot Permissions"
(Note: The Administrator Permission is likely overkill, but makes it easier for testing new functionality. Choose the permission with care when inviting the bot to a non-test server. At the current state the bot needs to be able to read, write and edit messages)

Your OpenAI Key can be found under https://platform.openai.com/api-keys <br>
Please note, that this version of the bot was tested with an api key of gpt-3.5 plus.

## Stopping the Container

To stop and remove the running IntraIntel bot container, execute the following command:

```bash
sudo docker stop intraintel
```

## Starting the python script directly
Instead of starting the docker container you can run the python script directly.
```bash
export OPENAI_API_KEY=your_openai_api_key
python3 main.py --token your_discord_api_key
```