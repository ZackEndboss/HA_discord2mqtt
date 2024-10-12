ARG BUILD_FROM
FROM $BUILD_FROM

ARG TEMPIO_VERSION BUILD_ARCH
RUN \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

# Install Borgmatic and BorgBackup with their dependencies
RUN \
    apk add --no-cache \
    borgbackup \
    py3-pip \
    openssh-client \
    openssh-keygen

RUN pip install --upgrade pip
RUN pip install borgmatic

WORKDIR /

RUN ssh-keygen -q -o -a 100 -t ed25519 -f ~/.ssh/id_ed25519 -C "hassio"

# Copy the run script
COPY run.sh /
RUN chmod a+x /run.sh

#ENTRYPOINT ["/run.sh"]
CMD ["/run.sh"]
