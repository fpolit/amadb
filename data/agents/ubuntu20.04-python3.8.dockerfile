FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y full-upgrade
RUN apt -y install python3.8 python3.8-dev python3-pymongo mongodb-server protobuf-compiler # required dependencies
RUN apt -y install python3-setuptools python3-pip git make cmake sudo # build dependencies

# python protobuf generation
RUN python3 -m pip install grpcio grpcio-tools

RUN useradd -m -u 970 jenkins && echo "jenkins:jenkins" | chpasswd
RUN echo "jenkins ALL=(root) NOPASSWD: $(which make)" >> /etc/sudoers
RUN visudo --check

# start mongodb server
RUN systemctld start mongodb

USER jenkins
