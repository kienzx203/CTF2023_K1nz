FROM php:7.4-apache
RUN docker-php-ext-install mysqli
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN a2enmod rewrite
COPY flag.txt /
WORKDIR /var/www/html
COPY . /var/www/html/
EXPOSE 80
CMD ["apache2-foreground"]
