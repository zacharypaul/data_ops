FROM node:18-alpine

WORKDIR /app

COPY package.json .
COPY package-lock.json* .

RUN npm install

EXPOSE 80

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "80"] 