docker-titan
============

Titan Docker Image

#build with: 
docker build --tag titan-cassandra .
# on OSX, make sure you map the port: 
VBoxManage modifyvm "boot2docker-vm" --natpf1 "tcp-port8182,tcp,,8182,,8182"
VBoxManage modifyvm "boot2docker-vm" --natpf1 "tcp-port8183,tcp,,8183,,8183"
VBoxManage modifyvm "boot2docker-vm" --natpf1 "tcp-port8184,tcp,,8184,,8184"

# run container with: 
docker run -d -p 8182:8182 -p 8183:8183 -p 8184:8184 titan-cassandra