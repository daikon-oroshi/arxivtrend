FROM asciidoctor/docker-asciidoctor

RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      harfbuzz \
      ca-certificates \
      ttf-freefont \
      nodejs \
      yarn
RUN apk add font-noto-cjk font-noto-emoji \
        terminus-font ttf-dejavu ttf-freefont ttf-font-awesome \
        ttf-inconsolata ttf-linux-libertine \
        && fc-cache -f

RUN yarn global add puppeteer @mermaid-js/mermaid-cli

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

ADD ./puppeteer-config.json /