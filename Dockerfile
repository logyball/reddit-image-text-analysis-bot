FROM alpine:latest

RUN apk add --update \
    python \
    libpython-dev \
    python-dev \
    py-pip \
    && pip install --upgrade setuptools  praw google-cloud-vision google-cloud-language

RUN mkdir code

COPY code/* code/

RUN python code/main.py &

# CMD [ "python", "code/main.py" ]