#!/bin/bash

echo "📥 Downloading and setting up trained models..."
echo ""

# Create trained_models directory if it doesn't exist
mkdir -p trained_models

# Download models if not present
if [ ! -f "trained_models.zip" ]; then
    echo "⬇️  Downloading trained_models.zip from S3..."
    wget https://d2hbdgqvbu3n3g.cloudfront.net/123sourcing/trained_models.zip
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to download models. Please check your internet connection."
        exit 1
    fi
    echo "✅ Download complete"
else
    echo "✅ trained_models.zip already exists"
fi

# Extract the models
if [ ! -d "trained_models/cpu-model" ] && [ ! -d "trained_models/gpu-model" ]; then
    echo ""
    echo "📦 Extracting models..."
    unzip -q trained_models.zip
    
    # Navigate to model directory and extract tar
    if [ -d "trained_models/cpu-model/model" ]; then
        echo "📦 Extracting CPU model parameters..."
        cd trained_models/cpu-model/model
    elif [ -d "trained_models/gpu-model/model" ]; then
        echo "📦 Extracting GPU model parameters..."
        cd trained_models/gpu-model/model
    else
        echo "❌ Model directory structure unexpected"
        exit 1
    fi
    
    if [ -f "docprompt_params.tar" ]; then
        tar -xf docprompt_params.tar
        echo "✅ Model parameters extracted"
    fi
    
    cd ../../..
    
    # Clean up zip file
    rm trained_models.zip
    echo "🧹 Cleaned up zip file"
else
    echo "✅ Models already extracted"
fi

echo ""
echo "✅ Trained models setup complete!"
echo ""
echo "📁 Models location: ./trained_models/"
