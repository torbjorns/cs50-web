# basing on a basic, public Dockerfile
FROM python:3 

# this is where I will store my app files in the container
COPY .  /usr/src/app 

# this is where I will run the following commands in the container
WORKDIR /usr/src/app 

# these are libraries that the container should install
RUN pip install -r requirements.txt

# these are the commands that start the server in the container
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]