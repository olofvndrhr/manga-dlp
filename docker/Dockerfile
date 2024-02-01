FROM git.44net.ch/44net/python311:11 AS builder

COPY pyproject.toml README.md /build/
COPY src /build/src
WORKDIR /build
RUN \
    echo "**** building package ****" \
    && pip3 install hatch hatchling \
    && python3 -m hatch build --clean

FROM git.44net.ch/44net/debian-s6:11

LABEL maintainer="Ivan Schaller" \
    description="A CLI manga downloader"

ENV PATH="/opt/python3/bin:${PATH}"

COPY --from=builder /opt/python3 /opt/python3
COPY --from=builder /build/dist/*.whl /build/dist/
COPY docker/rootfs /

RUN \
    echo "**** creating folders ****" \
    && mkdir -p /app \
    && echo "**** updating pip ****" \
    && python3 -m pip install --upgrade pip setuptools wheel \
    && echo "**** install python packages ****" \
    && python3 -m pip install /build/dist/*.whl

RUN \
    echo "**** cleanup ****" \
    && apt-get purge --auto-remove -y \
    && apt-get clean \
    && rm -rf \
    /tmp/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

WORKDIR /app
