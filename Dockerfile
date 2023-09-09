FROM python:3

WORKDIR /app

EXPOSE 80/tcp


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#RUN apk add --no-cache --upgrade bash
RUN rm -r migrations
#RUN bash dropdb.sh
ENV FLASK_APP="./project"
CMD ["bash", "deploy.sh"]
