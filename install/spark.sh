#!/usr/bin/env bash

# Install R
echo "deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/" | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get install r-base

