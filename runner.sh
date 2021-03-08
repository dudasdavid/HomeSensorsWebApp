#!/bin/bash

python3 -m http.server $HEALTHCHECK_PORT &
P1=$!
bash background_downloader.bash &
P2=$!
bokeh serve . --allow-websocket-origin='*' --port $SERVICE_PORT &
P3=$!
wait $P1 $P2 $P3
