FROM python:3.7-slim-buster

# Set the working directory
WORKDIR /app

# Copy the app files
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 unzip \
    && apt-get clean

# Pre-install CPU-specific PyTorch
RUN pip install torch==1.13.1+cpu torchvision==0.14.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu

# Install Python dependencies
RUN pip install -r requirements.txt

# Set the default command
CMD ["python3", "app.py"]
