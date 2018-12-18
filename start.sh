#!/usr/bin/env sh

# If the data folder is empty it is most likely because
# the container is fresh and has been started with
# the volume option
if ! [ "$(ls -A /usr/local/share/moin/data)" ]; then
    cp -r /usr/local/share/moin/bootstrap-data/* /usr/local/share/moin/data/
    chown -R www-data:www-data /usr/local/share/moin/data
else
    chmod g+x /usr/local/share/moin/data
    chown -R www-data:www-data /usr/local/share/moin/data
    find /usr/local/share/moin/data/ -type d -exec chmod g+s {} \;
fi

service rsyslog start && uwsgi \
    --uid www-data \
    --http-socket :8000 \
    --plugins python \
    --pidfile /var/run/uwsgi-moinmoin.pid \
    --wsgi-file server/moin.wsgi \
    -M -p 4 \
    --chdir /usr/local/share/moin \
    --python-path /usr/local/share/moin \
    --harakiri 30 \
    --die-on-term
