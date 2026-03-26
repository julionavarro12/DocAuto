FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --default-timeout=100 -r requirements.txt
    
CMD ["sh", "-c", "python scripts/generate_nav.py && mkdocs serve -a 0.0.0.0:8000"]