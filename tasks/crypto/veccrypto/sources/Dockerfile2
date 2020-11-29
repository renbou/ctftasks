FROM ubuntu:18.04

MAINTAINER tg: @renbou

RUN apt update -y && apt install -y --no-install-recommends \
    socat \
    python3.7 \
    python3-pip \
    && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install pycryptodome numpy
RUN mkdir -p /var/veccrypto

WORKDIR /var/veccrypto

ADD secret.py /var/veccrypto/secret.py
ADD server.py /var/veccrypto/server.py


CMD ["socat", "TCP-LISTEN:12345,reuseaddr,fork", "EXEC:\"python3 /var/veccrypto/server.py\""]
