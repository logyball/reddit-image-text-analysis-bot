FROM alpine:latest

RUN apk add --update \
    python \
    py-pip \
    && pip install praw

RUN mkdir code

COPY code/* code/

CMD [ "python", "code/main.py" ]