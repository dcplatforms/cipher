FROM python:3.12-slim

WORKDIR /app

RUN pip install requests pyyaml pydantic

COPY src/nist_sync.py /app/nist_sync.py

CMD ["python", "/app/nist_sync.py"]
