FROM node:10.16

# set working directory
WORKDIR /usr/src/app

COPY yarn.lock /usr/src/app/yarn.lock
COPY package.json /usr/src/app/package.json
COPY config-overrides.js /usr/src/app/config-overrides.js
ENV PATH $PATH:/usr/src/app/node_modules/.bin/

COPY . .

RUN yarn install

CMD ["yarn", "start"]
