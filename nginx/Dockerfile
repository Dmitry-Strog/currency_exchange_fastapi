FROM nginx:latest

USER root

# Копируем основной конфиг Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем фронтенд
COPY ./frontend /usr/share/nginx/html

CMD [ "nginx", "-g", "daemon off;" ]
