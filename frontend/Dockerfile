FROM apline:9.99
ARG APP_VERSION=1.0
ENV APP_MODE=production
RUN echo "Building frontend version: ${APP_VERSION}"
RUN rm -rf /usr/share/nginx/html/*
COPY ./index.html /usr/share/nginx/html/index.html
CMD ["nginx", "-g", "daemon off;"]