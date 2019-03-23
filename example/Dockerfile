FROM python:3.6.8-stretch

ARG port
ARG service

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN ln -s /root/.poetry/bin/poetry /bin/poetry
RUN poetry config settings.virtualenvs.create false

RUN mkdir /logs
RUN mkdir /app

COPY ./pyproject.toml /app
COPY ./poetry.lock /app
COPY ./example/runner.py /app

WORKDIR /app
RUN poetry install

# Note that example.py and the praetorian source directory need to be mounted
# as volumes

CMD ["python", "example.py", "--port=5000", "--logfile=/logs/example.log"]
