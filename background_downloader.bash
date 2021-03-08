#!/usr/bin/env bash

while [ true ]; do
    python3 background_downloader.py
    # Run in every 3 minutes
    sleep 180
done