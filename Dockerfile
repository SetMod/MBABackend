FROM python:3.9.18-alpine3.18

WORKDIR /app

RUN apk add --update --no-cache bind-tools

COPY . .

RUN pip install --no-cache-dir -r alpine-requirements.txt

CMD [ "python3", "app.py" ]
