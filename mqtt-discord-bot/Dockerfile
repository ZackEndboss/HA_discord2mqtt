ARG BUILD_FROM
FROM $BUILD_FROM
#FROM python:3.9-slim

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH
RUN \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

RUN \
    apk add --no-cache \
        python3 \
        py3-pip

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "./discord_mqtt.py"]
