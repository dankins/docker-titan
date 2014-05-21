#!/usr/bin/env python

import os
import socket
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

INTERNAL_IP=socket.gethostbyname(socket.gethostname())
REXSTER_BASE= "/opt/titan-server-0.4.2"
REXSTER_BIN = os.path.join(REXSTER_BASE,'bin/rexster.sh')
REXSTER_CONFIG_FILE = os.path.join(REXSTER_BASE,'conf/rexster-cassandra.xml')

# These are the Cassandra seed nodes for the cluster
# ideally this should come from etcd
SEEDS=os.getenv('SEEDS','172.17.42.1')

# open up the config file and load contents as YAML
xml = ET.ElementTree(file=REXSTER_CONFIG_FILE)

# get the properties element from the XML
graph = xml.iterfind('graphs/graph[0]').next()

for props in graph.iterfind('properties'):
	graph.remove(props)

# set new properties
props = ET.Element('properties')
ET.SubElement(props,'storage.backend').text = "cassandra"
ET.SubElement(props,'storage.backend').text = SEEDS
ET.SubElement(props,'storage.port').text = "9160"
ET.SubElement(props,'storage.connection-pool-size').text = "32"
ET.SubElement(props,'storage.replication-factor').text = "1"

graph.append(props)

# write out the new config
xml.write(REXSTER_CONFIG_FILE)

# Start Cassandra in the foreground.
os.execl(REXSTER_BIN,"rexster","-s","-wr","public","-c",REXSTER_CONFIG_FILE)
