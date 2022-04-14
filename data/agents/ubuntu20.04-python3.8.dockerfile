FROM ubuntu:20.04
# Python version  : 3.8
# C/CXX compilers : 9.

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y full-upgrade
RUN apt -y install python3.8 python3.8-dev python3-pymongo mongodb-server # required dependencies
RUN apt -y install python3-setuptools python3-pip python3.8-venv git make cmake sudo protobuf-compiler systemd # build dependencies

# create python virtual enviroment
RUN python3 -m venv env
ENV PATH="env/bin:$PATH"

# python protobuf generation
RUN python3 -m pip install grpcio grpcio-tools

RUN useradd -m -u 970 jenkins && echo "jenkins:jenkins" | chpasswd
RUN echo "jenkins ALL=(root) NOPASSWD: $(which make)" >> /etc/sudoers
RUN visudo --check

# start mongodb server
RUN systemctl start mongodb

USER jenkins
