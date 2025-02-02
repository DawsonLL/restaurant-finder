
# Use Google Cloud SDK's container as the base image
#FROM google/cloud-sdk

# Specify your e-mail address as the maintainer of the container image
#LABEL maintainer="longlam124@gmail.com"

# Copy the contents of the current directory into the container directory /app
#COPY . /app

# Set the working directory of the container to /app
#WORKDIR /app

# Install the Python packages specified by requirements.txt into the container
#RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && apt update --allow-releaseinfo-change -y && apt install -y python3-pip && pip3 install -r requirements.txt

# Set the parameters to the program
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app

###

# Use Google Cloud SDK's container as the base image
FROM google/cloud-sdk

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="longlam124@gmail.com"

# Install required packages
RUN apt-get update -y && \
    apt-get install -y curl gnupg apt-transport-https ca-certificates python3-venv python3-pip

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Create a virtual environment
RUN python3 -m venv /app/venv

# Install dependencies inside the virtual environment
RUN /app/venv/bin/pip install -r /app/requirements.txt

# Copy the rest of the application files into the container
COPY . /app

# Set the command to run the app with Gunicorn
EXPOSE 8080
#CMD ["/app/venv/bin/gunicorn", "--bind", ":$PORT", "--workers", "1", "--threads", "8", "app:app"]
CMD ["/bin/sh", "-c", "/app/venv/bin/gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 8 app:app"]

