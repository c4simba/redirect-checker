FROM python:3.8
RUN pip install --no-cache-dir poetry
WORKDIR /code
# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true --local
RUN poetry config experimental.new-installer false
RUN poetry install
WORKDIR /code/src

ENV PATH=/code/.venv/bin:$PATH \
    FLASK_DEBUG=1

CMD ["python", "test_server/main.py"]
