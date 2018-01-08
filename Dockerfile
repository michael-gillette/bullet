FROM python:3-alpine

WORKDIR /build

COPY . .

RUN pip install pipenv

RUN pipenv install

RUN pipenv install --system

RUN pip install --no-cache-dir .

ENTRYPOINT [ "/usr/local/bin/bullet" ]
CMD [ ]
