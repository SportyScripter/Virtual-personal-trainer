# # Stage 1: Build the React app
# FROM node:20-slim as build

# # Set the working directory in the container
# WORKDIR /app

# # Copy package.json and package-lock.json (or yarn.lock)
# COPY package.json ./
# COPY package-lock.json ./

# # Install dependencies
# RUN npm install

# # Copy the rest of your app's source code
# COPY . .

# # Expose the port Vite will run on
# EXPOSE 5173

# CMD ["npm", "run", "dev"]