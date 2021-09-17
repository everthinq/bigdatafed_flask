# init a base image (Alpine is small Linux distro)
FROM python:3.8.10-alpine

# upgrade pip
RUN pip install --upgrade pip

# define the present working directory
WORKDIR flask_xlstojson

# copy the contents into the working dir
ADD . /flask_xlstojson

# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt

# export FLASK_APP
ENV FLASK_APP=flask_xlstojson
ENV FLASK_RUN_HOST=0.0.0.0

# define the command to start the container
CMD ["flask", "run", "-p", "8080"]