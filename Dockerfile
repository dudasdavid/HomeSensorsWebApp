FROM python:3

# Setup start dir
WORKDIR /usr/src/app

# Set build arguments
ARG H_PORT
ARG S_PORT

# Set port ENV vars based on arguments
ENV HEALTHCHECK_PORT $H_PORT
ENV SERVICE_PORT $S_PORT

# Fix Python printing issue
ENV PYTHONUNBUFFERED true

# Expose network ports
EXPOSE $HEALTHCHECK_PORT
EXPOSE $SERVICE_PORT

# Create folders needed for favicon.ico 
RUN ["mkdir", "static"]
RUN ["mkdir", "templates"]

# Create folder for local db
RUN ["mkdir", "data"]

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy favicon.ico related files
COPY favicon.ico static/favicon.ico
COPY index.html templates/index.html

# Copy Firebase ceredntials
# ToDo: this should be moved to ENV
COPY home-sensors-credentials.json .

# Copy Python/shell helper libs
COPY SimpleLogger.py .
COPY app_hooks.py .
COPY background_downloader.py .
COPY background_downloader.bash .
COPY runner.sh .

# Fix execution permissions
#RUN ["chmod", "+x", "/usr/src/app/runner.sh"]

# Copy local db
COPY data/home_sensors_v1.csv data/home_sensors_v1.csv
# Update local db
RUN python background_downloader.py
# Copy main script
COPY main.py .
# Start runner.sh that will launch a few apps in the background
ENTRYPOINT ["sh","/usr/src/app/runner.sh"]