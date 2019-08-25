# Start with latest LTS of Ubuntu
FROM ubuntu:xenial
MAINTAINER Scott Essner <scott.essner@gmail.com>

# Install add-apt-repository from software-properties-common
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    python3 \
    python3-pip \
    python3-dev \
    gcc \
    git \
    locales \
    locales-all

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# After we installed software-properties-common, now we can add our ppa's for handbrake
RUN add-apt-repository ppa:stebbins/handbrake-releases \
    && add-apt-repository ppa:mc3man/xerus-media

# Install software from ppa's
RUN apt-get update && apt-get -y install --no-install-recommends \
    handbrake-cli \
    libavcodec-extra \
    ffmpeg \
    nfs-common \
    python3-mediainfodll

# Create the group and user to be used in this container
#RUN groupadd ssessner && useradd -m -g ssessner -s /bin/bash ssessner

# Create the working directory (and set it as the working directory)
RUN mkdir -p /opt/client
WORKDIR /opt/client

RUN mkdir -p /data

# Set up links to refer to python3 versions of python and pip
RUN cd /usr/bin \
    && ln -s python3 python \
    && ln -s pip3 pip

# Need to install setuptools to build from source distributions
RUN pip install setuptools

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY requirements.txt /opt/client
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /opt/client

#RUN chown -R ssessner:ssessner /home/ssessner
#
#USER ssessner

CMD ["python", "main.py"]


