FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install mkdocs

CMD ["sh", "-c", "python scripts/update_nav.py && mkdocs build"]