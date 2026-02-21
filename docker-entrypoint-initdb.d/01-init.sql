-- Инициализация базы данных YSSS
-- Этот скрипт запускается автоматически при первом запуске контейнера PostgreSQL

SELECT 'CREATE DATABASE ysss'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ysss')\gexec
