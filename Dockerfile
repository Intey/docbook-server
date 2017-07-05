FROM intey/flask
MAINTAINER churin@10205.ru
WORKDIR /home/webby
ENTRYPOINT ["./server.py", "8000"]

RUN apt-get update &&\
    apt-get install -y libsaxonb-java libxml2-utils fop make python3-lxml python3-yaml fonts-liberation

COPY node_modules /home/webby/node_modules
COPY build /home/webby/build
COPY static /home/webby/static
COPY templates /home/webby/templates
COPY server.py /home/webby/server.py
