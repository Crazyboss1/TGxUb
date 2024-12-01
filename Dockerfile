# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . /app/

# Specify the command to run your bot.py script
CMD ["python", "bot.py"]
