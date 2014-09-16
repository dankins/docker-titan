#!/usr/bin/env python

import os
import socket
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

INTERNAL_IP=socket.gethostbyname(socket.gethostname())
REXSTER_BASE= "/titan-server"
REXSTER_BIN = os.path.join(REXSTER_BASE,'bin/rexster.sh')
REXSTER_CONFIG_FILE = os.path.join(REXSTER_BASE,'conf/rexster-cassandra.xml')
REXSTER_BASE_URI = os.environ['REXSTER_BASE_URI']
REXSTER_PORT = os.getenv('REXSTER_PORT','8182')
AUTOTYPE = os.getenv('TITAN_AUTOTYPE','blueprints')
BATCH = os.getenv('TITAN_BATCH','true')

# These are the Cassandra seed nodes for the cluster
# ideally this should come from etcd
SEEDS=os.getenv('SEEDS','172.17.42.1')

# open up the config file and load contents as YAML
xml = ET.ElementTree(file=REXSTER_CONFIG_FILE)

xml.iterfind('http/base-uri').next().text = REXSTER_BASE_URI
xml.iterfind('http/server-port').next().text = REXSTER_PORT

# get the properties element from the XML
graph = xml.iterfind('graphs/graph[0]').next()

for props in graph.iterfind('properties'):
	graph.remove(props)

# set new properties
props = ET.Element('properties')
ET.SubElement(props,'autotype').text = AUTOTYPE
ET.SubElement(props,'storage.batch-loading').text = BATCH
ET.SubElement(props,'storage.backend').text = "cassandra"
ET.SubElement(props,'storage.hostname').text = SEEDS
ET.SubElement(props,'storage.port').text = "9160"
ET.SubElement(props,'storage.connection-pool-size').text = "32"
ET.SubElement(props,'storage.replication-factor').text = "1"

graph.append(props)

# write out the new config
xml.write(REXSTER_CONFIG_FILE)

# Start Cassandra in the foreground.
os.execl(REXSTER_BIN,"rexster","-s","-wr","public","-c",REXSTER_CONFIG_FILE)
