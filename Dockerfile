FROM alpine:latest

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    && pip install --upgrade setuptools praw google-cloud-vision google-cloud-language flask spotipy giphy_client

RUN mkdir code

COPY code/* code/

RUN python code/main.py &

CMD [ "python", "code/front_end.py" ]