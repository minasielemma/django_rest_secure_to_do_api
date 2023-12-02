# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /code/

# Expose the Django development server port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "localhost:8000"]
