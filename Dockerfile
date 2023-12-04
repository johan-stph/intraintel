FROM python:3.10-bullseye
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
ENV DISCORD_API_KEY=""
ENV OPENAI_API_KEY=""
CMD python3 main.py --token $DISCORD_API_KEY