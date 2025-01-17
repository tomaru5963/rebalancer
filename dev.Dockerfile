# syntax=docker/dockerfile:1
FROM python:3.11

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH
RUN poetry config virtualenvs.in-project true
