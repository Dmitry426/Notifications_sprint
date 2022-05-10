FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./workers/worker_email/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir services
RUN mkdir Configs
COPY ./services services
COPY ./Configs Configs
COPY ./workers .

CMD [ "python", "-m", "worker_email.listener"]
#CMD [ "python", "-m", "http.server"]