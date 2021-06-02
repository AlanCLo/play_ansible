FROM ubuntu:bionic

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /var/run/sshd

RUN apt-get -qq update -y \
 && apt-get -qq install -y apt-offline openssh-server \
 && apt-get -qq install -y python3 python3-apt python3-dev python3-pip \
 && apt-get -qq install -y vim \
 && apt-get -qq clean -y \
 && apt-get -qq purge -y \
 && rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

RUN mkdir /root/.ssh
COPY key.pub /root/.ssh/authorized_keys

WORKDIR /root
CMD ["/usr/sbin/sshd", "-D"]
