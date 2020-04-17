# HKJC analysis project

HKJC repo is a project fro analyzing the horse racing data from [HKJC](https://bet.hkjc.com/racing/index.aspx?lang=en)

## Contents
* [Prerequisites](#Prerequisites)
* [Installing](#Installing)
* [Crawler][#Crawler]

## Prerequisites
1. Download [Miniconda3](https://docs.conda.io/en/latest/miniconda.html)
```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
export PATH=~/miniconda/bin:$PATH
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

## Crawler
1. Get into the crawler directory
```bash
cd HKJC_crawler
```
2. Run the crawler and store into output.csv
```bash
scrapy crawl Odd_crawler -o output.csv
```
