FROM python:3.11-slim-bullseye as base
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install dependencies for OpenALPR
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    git \
    libcurl4-openssl-dev \
    liblog4cplus-dev \
    libopencv-dev \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install OpenALPR from source
RUN git clone https://github.com/openalpr/openalpr.git /opt/openalpr && \
    cd /opt/openalpr/src && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc .. && \
    make && \
    make install

# Install OpenALPR Python bindings from the source
RUN cd /opt/openalpr/src/bindings/python && \
    python setup.py install

# Install Python requirements
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
EXPOSE 8080

FROM base as local

FROM base as prod
COPY ./ ./
