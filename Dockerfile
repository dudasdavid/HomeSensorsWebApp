FROM python:3

WORKDIR /usr/src/app

ARG H_PORT
ARG S_PORT

ENV HEALTHCHECK_PORT $H_PORT
ENV SERVICE_PORT $S_PORT

EXPOSE $HEALTHCHECK_PORT
EXPOSE $SERVICE_PORT

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY runner.sh .
RUN ["chmod", "+x", "/usr/src/app/runner.sh"]

RUN ["mkdir", "data"]
COPY data/home_sensors_v1.csv data/home_sensors_v1.csv

ENV PYTHONUNBUFFERED true

COPY home-sensors-credentials.json .
COPY SimpleLogger.py .
COPY app_hooks.py .
COPY background_downloader.py .
COPY background_downloader.bash .

RUN python background_downloader.py

COPY main.py .
COPY favicon.ico /.
COPY index.html /.

#CMD [ "bokeh", "serve", "." ]

ENTRYPOINT ["sh","/usr/src/app/runner.sh"]