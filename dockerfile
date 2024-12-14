#using the official python base image

FROM python:3.9-slim

#set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies in the container
RUN pip install --no-cache-dir -r requirements.txt

# Download the spaCy English model
RUN python -m spacy download en_core_web_sm

#copy local script into container

COPY . .

EXPOSE 8000

#command to run the app
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]


