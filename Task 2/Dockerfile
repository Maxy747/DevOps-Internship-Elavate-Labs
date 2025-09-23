# Use an official Node.js runtime as a parent image
FROM node:18-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install app dependencies
RUN npm install

# Bundle app source
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define the command to run your app
CMD [ "npm", "start" ]