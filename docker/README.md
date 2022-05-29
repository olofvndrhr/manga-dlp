# Docker container of manga-dlp

## Quick start

> the pdf creation only works on amd64 images, as it unfortunately is incompatible with arm64.

```sh
# with docker-compose
curl -O docker-compose.yml https://raw.githubusercontent.com/olofvndrhr/manga-dlp/master/docker/docker-compose.yml
# adjust settings to your needs
docker-compose up -d

# with docker run
docker run -v ./downloads:/app/downloads -v ./mangas.txt:/app/mangas.txt olofvndrhr/manga-dlp
```

### Change UID/GID

> The default UID and GID are 4444.

You can change the UID and GID of the container user simply with:

```yml
# docker-compose.yml
environment:
  - PUID=<userid>
  - PGID=<groupid>
```

```sh
docker run -e PUID=<userid> -e PGID=<groupid>
```

## Run commands in container

> You don't need to use the full path of manga-dlp.py because `/app` already is the working directory

You can simply use the `docker exec` command to run the scripts like normal.

```sh
docker exec <container name> python3 manga-dlp.py <options>
```

## Run your own schedule

The default config runs `manga-dlp.py` once a day at 12:00 and fetches every chapter of the mangas listed in the file
`mangas.txt` in the root directory of this repo.

#### The default options used are:

```sh
--read mangas.txt
--chapters all
--path /app/downloads
--wait 2
```

To use your own schedule you need to mount (override) the default schedule or add new ones to the crontab.

> Don't forget to add the cron entries for every new schedule

```yml
# docker-compose.yml
volumes:
  - ./crontab:/etc/cron.d/01_mangadlp # overwrites the default crontab
  - ./crontab2:/etc/cron.d/02_something # adds a new one crontab file
  - ./schedule1:/app/schedules/daily # overwrites the default schedule
  - ./schedule2:/app/schedules/weekly # adds a new schedule
```

```sh
docker run -v ./crontab:/etc/cron.d/01_mangadlp # overwrites the default crontab
docker run -v ./crontab2:/etc/cron.d/02_something # adds a new one crontab file
docker run -v ./schedule1:/app/schedules/daily # overwrites the default schedule
docker run -v ./schedule2:/app/schedules/weekly # adds a new schedule
```

#### The default crontab file:

```sh
0 12 * * * root /app/schedule > /proc/1/fd/1 2>&1
```

## Add mangas to mangas.txt

If you use the default crontab you still need to add some mangas to mangas.txt. This is done almost identical to adding
your own cron schedule. If you use a custom cron schedule you need to mount the file you specified with `--read`.

```yml
# docker-compose.yml
volumes:
  - ./mangas.txt:/app/mangas.txt
```

```sh
docker run -v ./mangas.txt:/app/mangas.txt
```

## Change download directory

Per default as in the script, it downloads everything to "downloads" in the scripts root directory. This data does not
persist with container recreation, so you need to mount it. This is already done in the quick start section. If you want
to change the path of the host, simply change `./downloads/` to a path of your choice.

```yml
# docker-compose.yml
volumes:
  - ./downloads/:/app/downloads
```

```sh
docker run -v ./downloads/:/app/downloads
```

