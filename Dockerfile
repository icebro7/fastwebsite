FROM node:18.12.0-alpine3.16 as web

WORKDIR /opt/fastwebsite
COPY /web ./web
RUN cd /opt/fastwebsite/web && npm i --registry=https://registry.npmmirror.com && npm run build


FROM python:3.12-slim-bullseye

WORKDIR /opt/fastwebsite
ADD . .
COPY /deploy/entrypoint.sh .

RUN chmod +x /opt/fastwebsite/entrypoint.sh

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,id=core-apt \
    --mount=type=cache,target=/var/lib/apt,sharing=locked,id=core-apt \
    sed -i "s@http://.*.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
    && rm -f /etc/apt/apt.conf.d/docker-clean \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev bash nginx vim curl procps net-tools

# 安装poetry并配置，然后安装aiohttp、aiofiles、bs4和chardet
RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && poetry config virtualenvs.create false \
    && poetry add aiohttp aiofiles bs4 chardet

COPY --from=web /opt/fastwebsite/web/dist /opt/fastwebsite/web/dist
ADD /deploy/web.conf /etc/nginx/sites-available/web.conf
RUN rm -f /etc/nginx/sites-enabled/default \ 
    && ln -s /etc/nginx/sites-available/web.conf /etc/nginx/sites-enabled/ 

ENV LANG=zh_CN.UTF-8
EXPOSE 80

ENTRYPOINT [ "sh", "entrypoint.sh" ]