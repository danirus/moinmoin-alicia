# moinmoin-alicia

This repository extends [olavgg/moinmoin-wiki](https://github.com/olavgg/moinmoin-wiki) to enable the [MoinMoin-Alicia](https://github.com/danirus/moin-theme-alicia) theme in the running wiki.

![Screenshot of MoinMoin with Alicia Theme](https://github.com/danirus/moinmoin-alicia/blob/master/screenshot.png)

Docker image with the Moinmoin wiki engine, uwsgi, nginx and self signed SSL.
Everything included with minimum fuzz and just works.

You can automatically download and run this with the following command:
    
    $ sudo docker run -d -p 443:443 -p 80:80 --name my_wiki danirus/moinmoin-alicia
    
Default superuser is `mmAdmin`, you activate him by creating a new user named `mmAdmin` and set your prefered password.

Volumes are also supported if you want to simplify backup with rsync or ZFS snapshots

    $ sudo docker run -d -p 443:443 -p 80:80 \
    >             -v moinmoin-data:/usr/local/share/moin/data \
    >             --name my_wiki danirus/moinmoin-alicia

## Copy wiki data

Use your previous wiki data: Create a volume, Mount it in a helper container, copy the previous wiki data to it, and run the container.

    $ docker volume create moinmoin-data
    $ docker run -v moinmoin-data:/data --name helper busybox true
    $ docker cp previous-wiki-data-dir/. helper:/data
    $ docker rm helper
    $ docker run -d -p 443:443 -p 80:80 \
    >        -v moinmoin-data:/usr/local/share/moin/data \
    >        --name my_wiki danirus/moinmoin-alicia

## Copy underlay pages

If you want to also copy the system pages from your original wiki, it's not necessary to keep them in an external volume, just copy them and adapt the permissions in the container's directory:

    $ cd into_your_wikis_underlay_dir
    $ docker cp . my_wiki:/usr/local/share/moin/underlay
    $ docker exec -it my_wiki /bin/bash
    root@2be8553ae916:/# cd /usr/local/share/moin/underlay
    root@2be8553ae916:/usr/local/share/moin/underlay# chown -R www-data:www-data .
    root@2be8553ae916:/usr/local/share/moin/underlay# find ./ -type d -exec chmod g+s {} \;
    (Ctrl + P + Q)

## NOTE

Since MoinMoin version 1.9.10 the default security settings became more strict. This Docker release has a much more relaxed security defaults. [Please read the changes](https://github.com/moinwiki/moin-1.9/blob/1.9.10/docs/CHANGES#L13).


## MoinMoin configuration

MoinMoin has many different configuration options, you can configure this by forking this project, edit the wikiconfig.py file and rebuild the docker image.


### Disable HTTPS / SSL

If you do not need HTTPS you can disable it by passing the -e NOSSL environment variable

    $ sudo docker run -d -p 80:80 -e NOSSL=1 --name my_wiki danirus/moinmoin-alicia

Pull requests are very welcome.

