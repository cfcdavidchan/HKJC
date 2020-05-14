import sys, os, subprocess
# get the crawler path
current_path = os.getcwd()
project_path = os.path.dirname(current_path)
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


