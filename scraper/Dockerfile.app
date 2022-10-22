FROM python:3.8
RUN pip install --upgrade pip

ENV INSTALL_DIR /home/web-scrapper-microservice
RUN mkdir -p $INSTALL_DIR
WORKDIR $INSTALL_DIR

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x app-entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./app-entrypoint.sh"]