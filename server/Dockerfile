FROM python:3.9
RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"]
