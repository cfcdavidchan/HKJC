import os, subprocess
# get the crawler path
project_path = os.getcwd()
crawler_path = os.path.join(project_path, 'HKJC_crawler')


def crawl_Course():
    commnad = 'python -c "import crawler;crawler.crawl_Course()"'
    subprocess.Popen(commnad, shell=True, cwd=crawler_path, executable="/bin/bash").wait()

def crawl_Hourse():
    commnad = 'python -c "import crawler;crawler.crawl_Horse()"'
    subprocess.Popen(commnad, shell=True, cwd=crawler_path, executable="/bin/bash").wait()

def crawl_Jockeys():
    commnad = 'python -c "import crawler;crawler.crawl_Jockeys()"'
    subprocess.Popen(commnad, shell=True, cwd=crawler_path, executable="/bin/bash").wait()

def crawl_Trainer():
    commnad = 'python -c "import crawler;crawler.crawl_Trainer()"'
    subprocess.Popen(commnad, shell=True, cwd=crawler_path, executable="/bin/bash").wait()

def crawl_Match():
    commnad = 'python -c "import crawler;crawler.crawl_Match()"'
    subprocess.Popen(commnad, shell=True, cwd=crawler_path, executable="/bin/bash").wait()


def crawl_RecentMatch():
    commnad = 'python -c "import crawler;crawler.crawl_RecentMatch()"'
    subprocess.Popen(commnad, shell=True, cwd=crawler_path, executable="/bin/bash").wait()

def crawl_Draw():
    commnad = 'python -c "import crawler;crawler.crawl_Draw()"'
    subprocess.Popen(commnad, shell=True, cwd=crawler_path, executable="/bin/bash").wait()

if __name__ == '__main__':
    crawl_Trainer()
    print ('Finish Crawl Trainers')
    crawl_Jockeys()
    print('Finish Crawl Jockeys')
    crawl_Hourse()
    print('Finish Crawl Hourse')
    crawl_Match()
    print('Finish Crawl Match')
    crawl_RecentMatch()
    print('Finish Crawl RecentMatch')
    crawl_Draw()
    print('Finish Crawl Draw')

    project_path = os.getcwd()
    google_spreadsheet_path = os.path.join(project_path, 'google_spreadsheet')
    commnad = 'python update_spreadsheet.py'
    subprocess.Popen(commnad, shell=True, cwd=google_spreadsheet_path, executable="/bin/bash").wait()

    print('Finish sending data to Google')
