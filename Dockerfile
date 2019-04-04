# spbootdocker
#
# VERSION 1.0
FROM registry.acs.aliyun.com/open/java8:4.0.0

MAINTAINER jackrain

COPY acs /acs

RUN mkdir -p /acs/src

RUN mkdir -p /acs/logs

RUN echo "pybootdocker setup"

RUN rpm --rebuilddb && yum -y install python

WORKDIR /opt

RUN wget -q https://files.pythonhosted.org/packages/b0/d1/8acb42f391cba52e35b131e442e80deffbb8d0676b93261d761b1f0ef8fb/setuptools-40.6.2.zip

RUN unzip -q /opt/setuptools-40.6.2.zip -d /opt

WORKDIR /opt/setuptools-40.6.2

RUN python setup.py install

RUN pip install -r /acs/requirements.txt

WORKDIR /acs

ENTRYPOINT ["/acs/acsstart"]

RUN echo "pybootdocker run"