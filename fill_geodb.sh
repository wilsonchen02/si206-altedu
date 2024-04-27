#!/bin/bash

# Fill up states and cities tables

# Permissions
chmod 777 ./get_us_regions.py
chmod 777 ./get_us_cities.py

# states first (6 times to fill up table)
for i in $(seq 1 6); do
    python3 get_us_regions.py
done

echo Finished populating states table

# cities second (150 times to fill up table)
for i in $(seq 1 150); do
    python3 get_us_cities.py
done

echo Finished populating cities table
