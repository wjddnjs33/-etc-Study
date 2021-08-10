FROM node:latest
COPY . /app
WORKDIR /app

ENV PORT 27893

RUN apt-get update
RUN apt-get upgrade -y

RUN npm install express playwright fs request ejs --save

RUN chmod u+r+x /app/entrypoint.sh
ENTRYPOINT /app/entrypoint.sh

EXPOSE 27893