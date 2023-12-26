FROM php:7.3-apache
COPY php.ini /usr/local/etc/php/
RUN apt-get update \
  && apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libpng-dev libmcrypt-dev \
  && docker-php-ext-install pdo_mysql mysqli mbstring gd iconv\
  && apt-get install -y libapache2-mod-security2 && a2enmod headers
#COPY ./modsecurity.conf /etc/modsecurity/modsecurity.conf
RUN rm -rf /var/lib/apt/lists/* /tmp/*
#CMD service apache2 restart
