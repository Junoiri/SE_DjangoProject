# Use the official Python 3.12 image as the base image
FROM python:3.12

# Install Git inside the container to clone the repository
RUN apt-get update && apt-get install -y git

# Clone your Django project from GitHub
RUN git clone https://github.com/Junoiri/SE_DjangoProject.git

# Set the working directory inside the container (adjust if necessary)
WORKDIR /SE_DjangoProject

# Install dependencies from the requirements file
RUN pip install -r requirements.txt

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the port on which the Django app will run
EXPOSE 9999

# Define the command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:9999"]
