# home-sensors-web-app

## Help setting up Google Firestore:
https://medium.com/faun/getting-started-with-firebase-cloud-firestore-using-python-c6ab3f5ecae0

## home-sensors-credentials.json
You will need a home-sensors-credentials.json file from Firstore to authenticate into Firestore.

## Setup steps:
1) Run background_downloader.py locally to have an up-to-date database

2) Build Docker image:
docker build -t ddudas/sensor-dashboard:latest --build-arg H_PORT=8124 --build-arg S_PORT=8123 .
docker build -t ddudas/sensor-dashboard:arm --platform linux/arm64 --build-arg H_PORT=8124 --build-arg S_PORT=8123 .

3) Test it locally:
docker run -p 8123:8123 -p 8124:8124 ddudas/sensor-dashboard:latest

You can open the local web app on http://localhost:8123/app

4) Push Docker image to the Docker hub:
docker push ddudas/sensor-dashboard:latest
docker push ddudas/sensor-dashboard:arm



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

Note: favicon.ico template:
https://stackoverflow.com/questions/47586873/where-should-i-put-favicon-ico-so-bokeh-serve-can-find-and-render-it

Create SSL cert:
https://hometechhacker.com/letsencrypt-certificate-dns-verification-noip/
sudo apt install certbot
sudo certbot certonly --manual --preferred-challenges dns -d home-sensors.ddns.net
ls /etc/letsencrypt/live/home-sensors.ddns.net/
    cert.pem  chain.pem  fullchain.pem  privkey.pem  README

In Oracle cloud load balancer:
Upload fullchain.pem as SSL Certificate File
And privkey.pem as Private Key File

https redirect:
https://blogs.oracle.com/cloud-infrastructure/http-url-redirect-on-oracle-cloud-infrastructure

Automate certificate renewal:
https://blog.cajo.info/2020/05/using-lets-encrypt-certificates-with.html#Step2
