FROM postgres:16

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Create the SQL file inside the image
RUN echo "CREATE USER hackathon WITH PASSWORD 'hackathon';" > /docker-entrypoint-initdb.d/init-hackathon.sql && \
    echo "CREATE DATABASE hackathon OWNER hackathon;" >> /docker-entrypoint-initdb.d/init-hackathon.sql
