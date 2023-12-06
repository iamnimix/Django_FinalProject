FROM python:3.11.4
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY . /backend

RUN pip install -r /backend/requirements.txt

RUN chmod +x /backend/server_entrypoint.sh
RUN chmod +x /backend/worker_entrypoint.sh
