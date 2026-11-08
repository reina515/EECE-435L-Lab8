# Lab 8: Docker Containers and Images

## What's in this folder

| Folder / file | What it is |
|---|---|
| `flask_docker/` | The Hello World Flask app used to build and run my first container |
| `image1_lab5_api/` | My Lab 5 users API (Postman and APIs), containerized on port 5000 |
| `image2_get_users/` | A small API with one GET endpoint, `get_users`, on port 3000 |
| `screenshots/` | All the screenshots for Activity 1 and Activity 2 |
| `Lab8.docx` | Word document with the screenshots and explanations |

## Activity 1: Hello World container

```powershell
cd flask_docker
docker image build -t flask_docker .
docker run -p 5000:5000 -d flask_docker
```

Open http://localhost:5000 and you should see `Hello World!`.

Docker gave the running container the random name `agitated_dhawan`. These are the commands I ran on it and what each one showed (screenshots are in `screenshots/`):

### `docker ps -a`

Lists every container on the machine, including stopped ones (without `-a` it only shows running ones).
In my output, the `flask_docker` container `agitated_dhawan` had status **Up 28 seconds**, was running the command `python3 app.py`, and had port `0.0.0.0:5000->5000/tcp`, meaning port 5000 on my laptop is forwarded to port 5000 inside the container.
The other rows are old containers from earlier labs, all with status **Exited**.

### `docker logs agitated_dhawan`

Shows everything the app inside the container printed to the terminal.
Mine showed Flask starting up (`Running on all addresses (0.0.0.0)` on port 5000), then two requests from my browser:
`GET / 200`, which is the Hello World page loading correctly, and `GET /favicon.ico 404`, which is just the browser asking for a tab icon the app doesn't have.
Because the container runs in the background (`-d`), this is the only way to see that output.

### `docker stop agitated_dhawan`

Stops the running container. Docker printed the container name back to confirm it.
Running `docker ps -a` again showed `agitated_dhawan` changed from **Up** to **Exited (137)**, and its port mapping disappeared because nothing is listening anymore.
The container isn't deleted, though: it still shows in the list and can be started again with `docker start agitated_dhawan`.

## Activity 2: Two images

Both images use the same name, `rgh22/lab8-reina_hani`, with two different tags.
Docker doesn't allow a colon inside a tag, so I used `0.0.1-RELEASE` and `0.0.2-RELEASE` instead of `0.0.1:RELEASE` and `0.0.2:RELEASE`.

### Image 1: Lab 5 API on port 5000 (tag 0.0.1-RELEASE)

```powershell
cd image1_lab5_api
docker build -t rgh22/lab8-reina_hani:0.0.1-RELEASE .
docker run -p 5000:5000 -d rgh22/lab8-reina_hani:0.0.1-RELEASE
```

| Method | Endpoint | What it does |
|---|---|---|
| GET | `/api/users` | Returns every user |
| GET | `/api/users/<user_id>` | Returns one user by id |
| POST | `/api/users/add` | Adds a new user from the JSON body |
| PUT | `/api/users/update` | Updates a user from the JSON body |
| DELETE | `/api/users/delete/<user_id>` | Deletes a user by id |

Test: `GET http://localhost:5000/api/users`

### Image 2: get_users API on port 3000 (tag 0.0.2-RELEASE)

```powershell
cd image2_get_users
docker build -t rgh22/lab8-reina_hani:0.0.2-RELEASE .
docker run -p 3000:3000 -d rgh22/lab8-reina_hani:0.0.2-RELEASE
```

| Method | Endpoint | What it does |
|---|---|---|
| GET | `/get_users` | Returns a list of the names of all users in the database |

Test: `GET http://localhost:3000/get_users` returns `["Reina "]`

## Notes

* All images use `python:3.13-alpine` so the package versions in `requirements.txt` install correctly.
* Each app runs Flask with `host="0.0.0.0"` so it can be reached from outside the container.
* `.dockerignore` keeps `venv/`, `__pycache__/` and screenshots out of the images.
* Both APIs use a small SQLite database (`database.db`) that is copied into the image.
