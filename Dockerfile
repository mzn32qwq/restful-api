FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY /app /app


# Install any needed packages specified in requirements.txt
RUN pip install Flask
RUN pip install PyJWT
RUN pip install requests


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run run.py when the container launches
ENTRYPOINT [ "python" ]

CMD ["auth_and_url_short.py"]

