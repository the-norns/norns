FROM python:alpine

LABEL \
  maintainer="grandquista@gmail.com" \
  name="norns" \
  version="0.1.0" \
  description="\
90s text game service\
"

EXPOSE 8000

WORKDIR /usr/src/app

COPY . .

RUN ./.docker/build.sh

CMD [ "./.docker/run.sh" ]
