FROM node:18.16-alpine

WORKDIR /frontend

COPY package*.json .

RUN npm install

COPY . ./

RUN npm run build

EXPOSE 8080

CMD sh -c "npm run serve -- --host"
