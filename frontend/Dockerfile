FROM node:20.1-bullseye-slim

WORKDIR /frontend

COPY . ./

RUN rm -rf node_modules && rm -f package-lock.json
RUN npm install && npm run build

EXPOSE 8080

CMD sh -c "npm run serve -- --host"
