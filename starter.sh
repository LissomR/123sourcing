#!/bin/bash

# Clone the repository
# git clone http://clone:<REPLACE_WITH_YOUR_TOKEN>@gitlab.sapidblue.in/ai-ml-automation/123sourcing.git

# Change directory to the cloned repository
cd 123sourcing

# Download the Trained Model from AWS S3
if [ ! -f "trained_models.zip" ]; then
  wget https://d2hbdgqvbu3n3g.cloudfront.net/123sourcing/trained_models.zip
fi


# Extract the Compressed Models Zip File for Utilization
if [ ! -d "trained_models" ]; then
  unzip trained_models.zip
  cd trained_models/gpu-model/model
  tar -xvf docprompt_params.tar
  cd ../../..
fi

# up docker-compose
docker-compose up -d
