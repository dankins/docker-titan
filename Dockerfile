# Titan
#
# VERSION               0.0.1
# BUILD-USING:        docker build -t titan .
# PUSH-USING:         docker tag titan quay.io/queue/titan  && docker push quay.io/queue/titan

FROM      quay.io/queue/base-jvm
MAINTAINER Dan Kinsley <dan@queuenetwork.com>

WORKDIR /opt
# download and install titan server
RUN wget --quiet http://s3.thinkaurelius.com/downloads/titan/titan-server-0.4.2.zip
RUN unzip -qq /opt/titan-server-0.4.2.zip
RUN chown daemon:daemon /opt/titan-server-0.4.2

ADD run.py /run.py
RUN chmod u+x /run.py
# Port for RexPro
EXPOSE 8182 8183 8184 8185

# Launch titan when launching the container
CMD ["/run.py"]
