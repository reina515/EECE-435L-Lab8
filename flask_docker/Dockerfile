# start from a small python image so we don't have to install python ourselves
FROM python:3.13-alpine

# copy only the requirements file first so docker can reuse this step if it didn't change
COPY ./requirements.txt /app/requirements.txt

# all the next commands will run inside the /app folder
WORKDIR /app

# install flask and the other packages the app needs
RUN pip install -r requirements.txt

# now copy the rest of our code into the image
COPY . /app

# when the container starts, run the hello world app
CMD ["python3", "app.py"]
