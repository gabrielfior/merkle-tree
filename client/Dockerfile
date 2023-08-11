# app/Dockerfile

FROM python:3.9

WORKDIR /app
COPY streamlit_app.py /app/streamlit_app.py
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]