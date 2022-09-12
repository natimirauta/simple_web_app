# simple_web_app
This is a simple/basic web app that, upon having the docker image built, it will open up port 80 for a simple web page with a button to click.
The reason for this application's existence is to be used in a K8s cluster as an example.

# Run the app
In order to test this application locally with Docker, follow the instructions:

First, create a Docker network for the frontend and backend of the application.

>docker network create webapp_network

Start the backend `redis` container.

>docker run -d --rm --name=redis --network=webapp_network -p 6379:6379 -v redis_data:/data redis

Start the frontend `simple_web_app` container.

>docker run -d --rm --name=simple_web_app --network=webapp_network -p 5000:80 -e APP_USER=Name ghcr.io/natimirauta/simple_web_app:main

After both frontend and backend containers are up and running, get the IP of the frontend container (`docker inspect simple_web_app`) and open a new tab in your browser with `<IP-of-the-frontend-container>:80`.

Stop the application and cleanup containers with:
>docker stop simple_web_app && docker stop redis
