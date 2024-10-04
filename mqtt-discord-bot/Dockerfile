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
    gcc \
    libc-dev \
    linux-headers \
    python3-dev \
    py3-pip

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

# Erstelle das Verzeichnis für den s6-Overlay-Service
RUN mkdir -p /etc/services.d/discord_bot

# Kopiere das Start-Skript in das Service-Verzeichnis
COPY run.sh /etc/services.d/discord_bot/run

# Mach das Start-Skript ausführbar
RUN chmod +x /etc/services.d/discord_bot/run


# Setze den s6-Overlay als CMD
# CMD ["/init"]

#CMD ["python", "./discord_mqtt.py"]
