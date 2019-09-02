FROM python:3.7-alpine

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev libxml2-dev libressl-dev libxslt-dev jpeg-dev zlib-dev
RUN pip install pip --upgrade

COPY requirements.txt /
RUN pip install -r requirements.txt
COPY requirements_dev.txt /
RUN pip install -r requirements_dev.txt

COPY src ./src/
COPY .env.example .env
COPY __main__.py .

ENTRYPOINT ["python3", "__main__.py"]
