# Titan
#
# VERSION               0.0.1
# BUILD-USING:        docker build -t titan .
# PUSH-USING:         docker tag titan quay.io/queue/titan  && docker push quay.io/queue/titan

FROM      quay.io/queue/base-jvm
MAINTAINER Dan Kinsley <dan@queuenetwork.com>

# download and install titan server
RUN curl --silent http://s3.thinkaurelius.com/downloads/titan/titan-server-0.4.2.zip --output titan-server.zip
RUN unzip -qq /titan-server.zip
RUN ln -s /titan-server-0.4.2 /titan-server
RUN chown daemon:daemon /titan-server

ADD run.py /run.py
RUN chmod u+x /run.py
# Port for RexPro
EXPOSE 8182 8183 8184 8185

# Launch titan when launching the container
CMD ["/run.py"]
