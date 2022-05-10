FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./websocket_server/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir Configs
COPY ./Configs Configs
COPY ./websocket_server .

CMD [ "python", "main.py"]
#CMD [ "python", "-m", "http.server"]