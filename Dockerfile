# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# make setup excecutable and run it
RUN chmod +x /app/setup.sh
RUN sh /app/setup.sh

# Define environment variable
ENV SERVER "192.168.2.1"

# Run app.py when the container launches
CMD ["python", "/app/note.py"]
