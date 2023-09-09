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
ENV FLASK_APP=project
ENV SECRET_KEY=test-string
ENV SQLALCHEMY_DATABASE_URI='postgresql://postgres:password@postgres_server:5432/test1'
CMD ["bash", "deploy.sh"]
