from flask import Flask

# create the flask app
app = Flask(__name__)


# shows a simple hello world message on the home page
@app.route("/")
def hello():
    return "Hello World!"


# start the server on port 5000, and 0.0.0.0 lets us reach it from outside the container
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
