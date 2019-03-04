import pdb
from selenium import webdriver
import pickle as pkl 

# with open('cookie.pkl', 'rb') as f:
#     cookie = pkl.load(f)

options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=/Users/allen/Codes/NLP_learning/Web_crawler/dyn_crawl")
driver = webdriver.Chrome(options=options)

# driver.get('http://www.dianping.com/shop/108298313')
# driver.add_cookie(cookie)
driver.get('http://www.dianping.com/shop/108298313')

pdb.set_trace()
driver.close()
print()