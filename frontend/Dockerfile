FROM node:22-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start Vite dev server - --host makes it reachable from outside container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
