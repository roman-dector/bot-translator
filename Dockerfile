FROM python:3.10.0-slim-buster

WORKDIR /bot-translator

COPY requirements.txt requirements.txt 

RUN pip3 install -r requirements.txt 

COPY . .

EXPOSE 5000
CMD ["python3", "bot/run_bot.py"]
