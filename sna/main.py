from selenium import webdriver
from . import config as c
import json
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

# create a new Firefox session
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
class ChromeDriver:
    def __init__(self,exe_path =c.CHROME_DRIVER_PATH):
        self.driver = webdriver.Chrome(executable_path=exe_path)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    @classmethod
    def new_chrome(cls):
        return ChromeDriver()

    def find_all_friends(self,username):
        if '|' in username:
            fetch_url = "https://facebook.com/"+username.split('|')[1]+"/friends"
        else:
            fetch_url = "https://facebook.com/"+username+"/friends"
        self.driver.get(fetch_url)
        l = 0
        last_l = -1
        friend_list = []
        while last_l != l:
            friends = self.driver.find_elements_by_class_name("_5qo4")
            print('Interpreting Data')
            for friend in friends[l:]:
                soup = BeautifulSoup(friend.get_attribute('innerHTML'), 'html.parser')
                divs = soup.find_all('div', {'class': 'fsl fwb fcb'})
                for div in divs:
                    name=div.get_text()
                    # print(name)
                    for a in div.find_all('a', href=True) :
                        link=a['href'][:a['href'].find('?')]
                        try:
                            user_id=json.loads(a['data-gt'])['engagement']['eng_tid']
                        except:
                            user_id='xxxx'
                    if user_id == 'xxxx':
                        break
                    friend_list.append((name,link,user_id))
            print('Scrolling Down')
            for i in range(20):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
            last_l = l
            l = len(friends)
            print(len(friend_list), 'friends were collected.')
        return friend_list

