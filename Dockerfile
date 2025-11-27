FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y apache2 python3 python3-pip libmariadb-dev \
    libapache2-mod-wsgi-py3 python3-dev openssh-client nano pkg-config \
    default-libmysqlclient-dev build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure timezone
ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# Application environment
WORKDIR /app

COPY ./videojuegos/requirements.txt /app/requirements.txt

RUN pip3 install --break-system-packages -r /app/requirements.txt

EXPOSE 8000

CMD ["python3", "videojuegos/manage.py", "runserver", "0.0.0.0:8000"]