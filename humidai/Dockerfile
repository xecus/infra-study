FROM ubuntu:16.04

RUN apt-get update && \
  apt-get install -y software-properties-common && \
  apt-get install -y vim htop jq iputils-ping net-tools wget curl unzip

RUN add-apt-repository ppa:gluster/glusterfs-3.12 && \
  apt-get update && apt-get install -y glusterfs-server glusterfs-client && \
  mkdir -p /glusterfs/distributed

RUN  apt-get install -y ipvsadm keepalived attr

RUN wget -O consul.zip https://releases.hashicorp.com/consul/0.9.3/consul_0.9.3_linux_amd64.zip \
  && unzip consul.zip && mv consul /bin/consul && rm consul.zip

RUN wget -O /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.13.0/confd-0.13.0-linux-amd64
RUN chmod +x /usr/local/bin/confd

RUN apt-get install -y python-pip && \
  pip install --upgrade pip && \
  pip install python-consul

RUN apt-get autoclean \
  && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

ADD confd /tmp/confd

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
