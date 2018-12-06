FROM ubuntu:18.04

RUN apt update
RUN apt install --upgrade -y \
    python3-pip \
    && pip3 install --upgrade setuptools praw google-cloud-vision google-cloud-language flask spotipy giphy_client

RUN mkdir code

COPY code/* code/

RUN python3 code/main.py &

CMD [ "python3", "code/front_end.py" ]
