FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./storage_consumers/websocket_consumer/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir services
RUN mkdir Configs
COPY ./Configs Configs
COPY ./services services
COPY ./storage_consumers .

CMD [ "python", "-m", "websocket_consumer.listener"]
#CMD [ "python", "-m", "http.server"]