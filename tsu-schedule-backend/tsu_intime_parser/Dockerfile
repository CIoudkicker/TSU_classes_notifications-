FROM python:3.9

# Set the working directory in the container
WORKDIR /tsu-intime-parser

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Expose a port that microservice will be listening on
EXPOSE 8000

# Define the command to run microservice
CMD ["python", "-u", "main.py"]
