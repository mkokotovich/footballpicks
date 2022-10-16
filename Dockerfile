FROM node:10.16 as uibuilder

# set working directory
WORKDIR /usr/src/app

COPY frontend/fbpicks/yarn.lock /usr/src/app/yarn.lock
COPY frontend/fbpicks/package.json /usr/src/app/package.json
COPY frontend/fbpicks/config-overrides.js /usr/src/app/config-overrides.js
ENV PATH $PATH:/usr/src/app/node_modules/.bin/
RUN yarn install

COPY frontend/fbpicks .

RUN yarn build

#==============================================

FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE footballpicks.settings.prod

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code/

RUN mkdir -p /static/www/
COPY --from=uibuilder /usr/src/app/build /static/www/

RUN python manage.py collectstatic --noinput --clear

EXPOSE 8000

# replace demo.wsgi with <project_name>.wsgi
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "footballpicks.wsgi"]
