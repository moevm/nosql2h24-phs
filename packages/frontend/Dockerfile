FROM node:20.3.0-alpine3.17

WORKDIR /app

COPY package.json ./

RUN npm cache clean --force

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD [ "npm", "run", "preview" ]