# spbootdocker
#
# VERSION 1.0
FROM registry.acs.aliyun.com/open/java8:4.0.0

MAINTAINER jackrain

COPY acs /acs

RUN mkdir -p /acs/src

RUN mkdir -p /acs/logs

WORKDIR /acs

RUN echo "spbootdocker setup"

# Expose the default port
EXPOSE 8080

ENTRYPOINT ["/acs/acsstart"]

RUN echo "spbootdocker run"