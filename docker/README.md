# Docker container of manga-dlp

> Full docs: https://manga-dlp.ivn.sh/docker

## Quick start

The pdf creation only works on amd64 images, as it unfortunately is incompatible with arm64.

```sh
# with docker-compose
curl -O docker-compose.yml https://raw.githubusercontent.com/olofvndrhr/manga-dlp/master/docker/docker-compose.yml
# adjust settings to your needs
docker-compose up -d

# with docker run
docker run -v ./downloads:/app/downloads -v ./mangas.txt:/app/mangas.txt olofvndrhr/manga-dlp
```
