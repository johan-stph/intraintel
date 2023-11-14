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
sudo docker run -d --name intraintel -e TOKEN="your_token_value" intraintel:latest
```

Replace `"your_token_value"` with the actual value you want to set for the `TOKEN` environment variable. This command starts the IntraIntel bot in detached mode within a Docker container.

## Stopping the Container

To stop the running IntraIntel bot container, execute the following command:

```bash
sudo docker stop intraintel
```

## Removing the Container

If you need to remove the stopped IntraIntel bot container, use the following command:

```bash
sudo docker rm intraintel
```

## Starting the python script directly
Instead of starting the docker container you can run the python script directly with
```bash
python3 main.py --token your_token_value
```