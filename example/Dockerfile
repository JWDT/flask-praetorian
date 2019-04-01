# Note that specific example to be built needs to be volume-mouted as
# /app/example.py and the praetorian source directory need to be volume-mounted
# as /app/flask_praetorian

FROM python:3.6.8-stretch

ARG port
ARG service

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN ln -s /root/.poetry/bin/poetry /bin/poetry
RUN poetry config settings.virtualenvs.create false

RUN mkdir /logs

RUN mkdir /app
WORKDIR /app
COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml
RUN poetry install
VOLUME /app

CMD ["flask", "run"]
