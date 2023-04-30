FROM python:3.10
WORKDIR /code
COPY ./ /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN python /code/db_create.py
RUN python /code/db_populate.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]