# Use an official Python runtime as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
COPY secure_to_do/.env /code/secure_to_do/.env
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /code/

# Expose the Django development server port
EXPOSE 8000

# Run the Django development server
# CMD ["daphne", "-b","0.0.0.0", "secure_to_do.asgi:application", "--port", "8000"]
