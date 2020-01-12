FROM node:11-alpine
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
# COPY ./src/package*.json ./
# RUN npm install
# COPY ./src ./
VOLUME ./src:/usr/src/app
EXPOSE 3000

# CMD ["npm", "run", "dev"]
CMD ["npm", "run", "start"]