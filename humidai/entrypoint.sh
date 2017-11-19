#!/bin/bash
set -ue

command=$1

if [ $command = "consul" ]; then
  mode=$2
  if [ $mode = "server" ]; then
    mkdir -p /tmp/consul /tmp/consul.d
    confd -onetime -backend env --confdir /tmp/confd/consul_server/
    /bin/consul agent -config-dir=/tmp/consul.d -server -bootstrap
  fi
  if [ $mode = "join" ]; then
    host=$3
    mkdir -p /tmp/consul /tmp/consul.d
    confd -onetime -backend env --confdir /tmp/confd/consul_server/
    /bin/consul agent -config-dir=/tmp/consul.d -server -join ${host}
  fi
fi

if [ $command = "gluster" ]; then
  host=$2
  mkdir -p /tmp/consul /tmp/consul.d
  confd -onetime -backend env --confdir /tmp/confd/gluster/
  glusterd
  /bin/consul agent -config-dir=/tmp/consul.d -join ${host}
fi


if [ $command = "keepalived" ]; then
  mkdir -p /tmp/keepalived
  confd -onetime -backend env --confdir /tmp/confd/keepalived_vrrp/
  #exec /usr/sbin/keepalived -f /tmp/keepalived/keepalived.conf -n --dont-fork --dump-conf --log-console --log-detail --vrrp
  exec /usr/sbin/keepalived -f /tmp/keepalived/keepalived.conf -n --dont-fork --dump-conf --log-console --log-detail --vrrp --check
fi

if [ $command = "do_nothing" ]; then
  while [ : ]; do
    sleep 1
  done
fi

