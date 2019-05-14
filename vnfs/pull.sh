#!/bin/bash
set -e

docker pull mpeuster/tng-bench-mp
docker pull mpeuster/vnf-calibration-stress
docker pull mpeuster/vnf-ids-suricata
docker pull mpeuster/vnf-ids-snort2
docker pull mpeuster/vnf-ids-snort3
docker pull mpeuster/vnf-lb-nginx
docker pull mpeuster/vnf-lb-haproxy
docker pull mpeuster/vnf-px-squid
docker pull mpeuster/vnf-broker-mosquitto
docker pull mpeuster/vnf-broker-hbmqtt
docker pull mpeuster/vnf-broker-emqx
docker pull mpeuster/vnf-ws-apache
