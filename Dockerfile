# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install the dependencies from requirements.txt
RUN pip install Flask
RUN pip install Flask-WTF
RUN pip install WTForms
RUN pip install Flask-SQLAlchemy
RUN pip install PyMySQL

# Copy the rest of your application code into the container
COPY . /app/

# Expose the port that Flask will run on
EXPOSE 5000

# Set the command to run your app
CMD ["python", "main.py"]