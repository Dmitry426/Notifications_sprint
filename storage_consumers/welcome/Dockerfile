FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./storage_consumers/welcome/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir services
RUN mkdir templates
RUN mkdir Configs
COPY ./services services
COPY ./templates templates
COPY ./Configs Configs
COPY ./storage_consumers .

CMD [ "python", "-m", "welcome.listener"]
#CMD [ "python", "-m", "http.server"]