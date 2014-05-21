# Titan
#
# VERSION               0.0.1
# BUILD-USING:        docker build -t docker-titan .

FROM      ubuntu
MAINTAINER Dan Kinsley <dan@watchtello.com>

# make sure the package repository is up to date
RUN apt-get update
# software-properties are so we can run "add-apt-repository"
RUN apt-get install -y wget unzip software-properties-common python-software-properties supervisor

# repository for java7
RUN add-apt-repository ppa:webupd8team/java

# update to add the new repository
RUN apt-get update 
# accept license without requiring user intervention
RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
# and now install oracle java7
RUN sudo apt-get update && apt-get install -y oracle-java7-installer

WORKDIR /opt
# download and install titan server
RUN wget --quiet http://s3.thinkaurelius.com/downloads/titan/titan-server-0.4.2.zip
RUN unzip -qq /opt/titan-server-0.4.2.zip
RUN chown daemon:daemon /opt/titan-server-0.4.2


# run memcached as the daemon user
#USER daemon

ADD run.py /run.py
RUN chmod u+x /run.py
# Port for RexPro
EXPOSE 8182 8183 8184 8185

# Launch titan when launching the container
CMD ["/run.py"]
