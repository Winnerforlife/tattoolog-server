FROM python:3.11

# Install necessary dependencies
RUN pip install --no-cache-dir django-environ

# Other environment setup
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy and install requirements
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade pip
RUN pip cache purge
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /code/
