FROM python:3.8

COPY Pipfile /code/Pipfile
COPY Pipfile.lock /code/Pipfile.lock
COPY ./app /code/app

RUN pip install pipenv

WORKDIR /code

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]