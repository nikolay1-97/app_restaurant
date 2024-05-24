FROM python:3.8

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY pyproject.toml .

RUN pip install --upgrade pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . .

RUN chmod a+x scripts_for_docker/*.sh

#WORKDIR app

#CMD ["poetry", "run", "uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8000"]