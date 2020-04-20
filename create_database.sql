CREATE DATABASE HKJC;
CREATE USER HKJC_user WITH PASSWORD '0123456789';
ALTER ROLE HKJC_user SET client_encoding TO 'utf8';
ALTER ROLE HKJC_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE HKJC_user SET timezone TO 'Asia/Hong_Kong';
GRANT ALL PRIVILEGES ON DATABASE HKJC TO HKJC_user;
