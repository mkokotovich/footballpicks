FROM node:10

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY yarn.lock /usr/src/app/yarn.lock
COPY package.json /usr/src/app/package.json
ENV PATH $PATH:/usr/src/app/node_modules/.bin/
RUN yarn install

COPY . .

CMD ["yarn", "start"]
