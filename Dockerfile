FROM python:3.9-buster

# Update package list and install necessary packages
# installing netcat for debugging and monitoring the network
# here used to check whether the postgres service  is listening in port 5432
RUN apt-get update && apt-get install -y libpq-dev netcat

# Upgrade pip
RUN pip install --upgrade pip

# set the working directory
WORKDIR /usr/src/app

# copy and install dependencies
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN pip3 freeze > requirements.txt

# copy application code
COPY . .

COPY entrypoint.sh ./

# Ensuring the entrypoint script is executable
RUN chmod +x entrypoint.sh

#Expose port 8001
EXPOSE 8001

ENTRYPOINT [ "entrypoint.sh" ]
