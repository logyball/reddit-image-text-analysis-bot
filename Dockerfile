FROM alpine:latest

RUN apk add --update \
    python \
    py-pip \
    && pip install --upgrade praw google-cloud-vision google-cloud-language

RUN mkdir code

COPY code/* code/

CMD [ "python", "code/main.py" ]