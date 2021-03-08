# home-sensors-web-app

## Help setting up Google Firestore:
https://medium.com/faun/getting-started-with-firebase-cloud-firestore-using-python-c6ab3f5ecae0

## home-sensors-credentials.json
You will need a home-sensors-credentials.json file from Firstore to authenticate into Firestore.

## Setup steps:
1) Run backround_downloader.py locally to have an up-to-date database

2) Build Docker image:
docker build -t ddudas/sensor-dashboard:latest --build-arg H_PORT=8124 --build-arg S_PORT=8123 .

3) Test it locally:
docker run -p 8123:8123 -p 8124:8124 ddudas/sensor-dashboard:latest

You can open the local web app on http://localhost:8123/app

4) Push Docker image to the Docker hub:
docker push ddudas/sensor-dashboard:latest



In hosted cloud environment:

1) Sign in if Dockerhub repository is private:
docker login --username=ddudas

2) Pull the latest image:
docker pull ddudas/sensor-dashboard:latest

3) Run in it detached mode:
docker run --name sensors -d -p 8123:8123 -p 8124:8124 ddudas/sensor-dashboard:latest

4) Other tools:
docker logs sensors --follow
docker kill sensors
docker container prune
