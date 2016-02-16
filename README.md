# pycrawler_weibo
This library is written for crawling Sina Weibo due to extremely unfriendly Sina API.  
At the time, pycrawler_weibo only supports crawling on searching certain keyword.

##Prerequisite
  - Python 2.7
    - https://www.python.org/downloads/
  - Beautifulsoup4
    - http://www.crummy.com/software/BeautifulSoup/bs4/
    - `pip install beautifulsoup4`
  - MySQL-python (option)
    - `pip install mysql-python`

## Simple Usage
  1. Open \_\_init\_\_.py and
    - edit login information and topic/mention
    - setup MySQL (MySQL)
  2. Go to working directory in terminal  
    `cd ~/...`
  3. Run \_\_init\_\_.py  
    `python __init__.py`

## Clases
- class  WeiboCrawler(isConnectMySQL=True, htmlOutputDir='')
  - search(keyword, pages=range(1, 51)
    - param keyword: (str/list) search keyword
    - param pages:   (int/list) pages of search
