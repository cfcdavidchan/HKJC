# HKJC analysis project

HKJC repo is a project fro analyzing the horse racing data from [HKJC](https://bet.hkjc.com/racing/index.aspx?lang=en)

## Contents
* [Prerequisites](#Prerequisites)
* [Installing](#Installing)
* [Crawler](#Crawler)

## Prerequisites
1. Download [Miniconda3](https://docs.conda.io/en/latest/miniconda.html)
```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
export PATH=~/miniconda/bin:$PATH
```

2. Download [PostgreSQL 11](https://www.postgresql.org/)
```bash
sudo apt-get install postgresql-11 postgresql-contrib
```

## Installing
1. Clone the repo
```bash
git clone git@github.com:cfcdavidchan/HKJC.git
```
2. Creating conda environment for the project and activate it
```bash
conda env create -f environment.yml
conda activate HKJC
```
3. Create PostgresSQL database
```bash
sudo su - postgres
psql
\i repo_path/create_database.sql
```
Note: repo_path means the full path of this repo in your local computer

## Crawler
1. Add going data into Database
```bash
python ./HKJC_database/going.py
```
2. Get into the crawler directory
```bash
cd HKJC_crawler
```
3. Run the crawler and store into PostgreSQL
```bash
scrapy crawl Course_crawler #crawl course data into Database
scrapy crawl Jockeys_crawler #crawl jockey data into Database
scrapy crawl Trainer_crawler #crawl trainer data into Database
scrapy crawl Horse_crawler #crawl horse data into Database
scrapy crawl Match_crawler #crawl Match data into Database
```
