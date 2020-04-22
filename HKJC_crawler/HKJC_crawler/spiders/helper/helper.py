import sys, os

base_path = os.path.realpath(__file__)
base_path = os.path.dirname(base_path)
global chrome_path
chrome_path = os.path.join(base_path, 'chromedriver')

def get_chrome_path():
    return chrome_path

if __name__ == "main":
    pass