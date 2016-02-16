# pycrawler_weibo
This library is written for crawling Sina Weibo due to extremely unfriendly Sina API.  
At the time, pycrawler_weibo only supports crawling on searching certain keyword.

### Prerequisite
  - [Python 2.7] (https://www.python.org/downloads/)
  - [Beautifulsoup4] (http://www.crummy.com/software/BeautifulSoup/bs4/)
    - `pip install beautifulsoup4`
  - [MySQL-python] (http://mysql-python.sourceforge.net/) *(option)*
    - `pip install mysql-python`

### Simple Usage
  1. Open test.py and
    - edit login information and topic/mention
    - setup MySQL *(option)*
  2. Go to working directory in terminal  
    `cd ~/...`
  3. Run test.py  
    `python __init__.py`

### Clases
- *class* WeiboCrawler(isConnectMySQL=True, htmlOutputDir='')
  - *def* search(keyword, pages=range(1, 51))
    - *param* keyword: (str/list) search keyword
    - *param* pages: (int/list) pages of search
  
