FROM python:3.7-slim
WORKDIR /backend
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]