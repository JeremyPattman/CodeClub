# CodeClub - Portal

## Build the docker image for the portal

docker build -t snakeportal:0.1 .

## Run the docker image for the portal
docker run -d -p 5000:5000 snakeportal:0.1

## Access the Portal
Open browser and enter http://localhost:5000/
