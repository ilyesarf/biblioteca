FROM nginx:latest

COPY wait-for-it.sh .

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy all static assets (js, css, images, etc.)
COPY ./static/ /usr/share/nginx/html/static/

# Copy all template HTML files to the root html directory
COPY ./templates/ /usr/share/nginx/html/

# Optionally copy entrypoint if needed
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

CMD ["/entrypoint.sh"]
