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

# let docker know the app listens on port 3000
EXPOSE 3000

# when the container starts, run the get_users api
CMD ["python3", "app.py"]
