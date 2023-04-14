FROM python:3.8

COPY Pipfile /code/Pipfile
COPY Pipfile.lock /code/Pipfile.lock
COPY . /code/omnibridge_api/

RUN pip install pipenv

WORKDIR /code

RUN pipenv install --system --deploy --ignore-pipfile
RUN pipenv update

CMD ["uvicorn", "omnibridge_api.app.main:app", "--host", "0.0.0.0", "--port", "80"]