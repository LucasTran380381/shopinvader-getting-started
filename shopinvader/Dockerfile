FROM node:18-alpine

WORKDIR /app/template

# Install git and necessary build tools
RUN apk add --no-cache git python3 make g++ curl

# Copy package files first (for better caching)
COPY template/package*.json template/yarn*.lock ./

# Set npm config to use HTTPS instead of SSH for git dependencies
RUN git config --global url."https://github.com/".insteadOf git@github.com: && \
    git config --global url."https://".insteadOf git:// && \
    yarn install

# Copy rest of the code
COPY template/ .

EXPOSE 3000

CMD ["yarn", "dev"]