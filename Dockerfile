# spbootdocker
#
# VERSION 1.0
FROM registry.acs.aliyun.com/open/java8:4.0.0

MAINTAINER jackrain

COPY acs /acs

RUN mkdir -p /acs/src

RUN mkdir -p /acs/logs

RUN echo "pybootdocker setup"

RUN yum install https://centos7.iuscommunity.org/ius-release.rpm -y

RUN yum install python36u -y

RUN ln -s /usr/bin/python3.6 /bin/python3

RUN yum install python36u-pip -y

RUN ln -s /usr/bin/pip3.6 /bin/pip3

RUN pip3 install -r /acs/requirements.txt

WORKDIR /acs

ENTRYPOINT ["/acs/acsstart"]

RUN echo "pybootdocker run"