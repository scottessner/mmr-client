# Start with latest LTS of Ubuntu
FROM python:3.5.6
MAINTAINER Scott Essner <scott.essner@gmail.com>

# Create the group and user to be used in this container
RUN groupadd ssessner && useradd -m -g ssessner -s /bin/bash ssessner

# Create the working directory (and set it as the working directory)
RUN mkdir -p /home/ssessner/client
WORKDIR /home/ssessner/client

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY requirements.txt /home/ssessner/client
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /home/ssessner/client

RUN chown -R ssessner:ssessner /home/ssessner

USER ssessner


