FROM python:3.7-alpine

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    libxml2-dev \
    libressl-dev \
    libxslt-dev \
    # pillow dependencies
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    # cairo dependencies
    cairo-dev \
    cairo \
    cairo-tools

RUN pip install pip --upgrade

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY src ./src/
COPY .env.example .env
COPY __main__.py .

ENTRYPOINT ["python3", "__main__.py"]
