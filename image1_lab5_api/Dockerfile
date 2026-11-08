
FROM python:3.13-alpine

# copy only the requirements file first so docker can reuse this step if it didn't change
COPY ./requirements.txt /app/requirements.txt

# all the next commands will run inside the /app folder
WORKDIR /app

# install flask and the other packages the app needs
RUN pip install -r requirements.txt

# now copy the rest of our code into the image
COPY . /app

# let docker know the app listens on port 5000
EXPOSE 5000

# when the container starts, run the lab 5 users api
CMD ["python3", "app.py"]
