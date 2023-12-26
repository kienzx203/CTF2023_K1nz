FROM httpd:2.4.49

COPY flag.txt /flag

RUN mv /flag /flag_`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 4 | head -n 1`

RUN echo "<VirtualHost *:80>\n \
    DocumentRoot /var/www/html/\n \
    <Directory \"/\">\n \
    Require all granted\n \
    </Directory>\n \
    </VirtualHost>" > /usr/local/apache2/conf/apache.conf

COPY httpd.conf /usr/local/apache2/conf/httpd.conf

RUN echo "Include /usr/local/apache2/conf/apache.conf" >> /usr/local/apache2/conf/httpd.conf

