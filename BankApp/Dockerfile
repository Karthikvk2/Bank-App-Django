
FROM python:3.9-slim


WORKDIR /app


COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "BankApp.wsgi:application"]
