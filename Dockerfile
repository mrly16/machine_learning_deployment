# set base image (host OS)
FROM python:3.8-slim-buster

# set the working directory in the container
WORKDIR /

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ /src/
RUN mkdir /models/
COPY app.py /
COPY config.py /
COPY constant.py /
COPY config.ini /

EXPOSE 5000

## command to run on container start
CMD ["python", "app.py"]
