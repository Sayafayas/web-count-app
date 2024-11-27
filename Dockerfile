FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install dependencies
RUN pip install flask pymysql python-dotenv --no-cache-dir

# Specify the command to run the app
CMD ["python", "app.py"]
