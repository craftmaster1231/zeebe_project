# Используем официальный образ PostgreSQL
FROM postgres:15

# Устанавливаем переменные окружения для PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres

# Копируем скрипт SQL для создания таблиц и заполнения данных
COPY init.sql /docker-entrypoint-initdb.d/

# Устанавливаем права доступа
RUN chmod 644 /docker-entrypoint-initdb.d/init.sql
