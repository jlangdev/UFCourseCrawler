from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate
import os
import time
import json

#launch url
url = "https://one.uf.edu/soc/"

# create a new chrome session
driver = webdriver.Chrome('./chromedriver.exe')
driver.get(url)

#click login
login_menu_button = driver.find_element_by_xpath('//*[@id="menu_container_0"]/md-menu-content/md-menu-item[1]/button') #login
driver.execute_script('arguments[0].click();', login_menu_button) #click login button

field_username = driver.find_element_by_xpath('//*[@id="username"]') #user
field_password = driver.find_element_by_xpath('//*[@id="password"]') #password
login_button = driver.find_element_by_xpath('//*[@id="submit"]') #password

#input user name and password
user_username = input('username: ')
user_password = input('password: ')

#populate login fields
field_username.send_keys(user_username)
field_password.send_keys(user_password)
login_button.click()

#get JSON response of degree audit
url = 'https://one.uf.edu/api/newdegreeaudit/loaddegreeaudit/'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
audit = json.loads(soup.find('body').text)

#requiremnts part of the JSON
data = audit['careers'][0]['planGroups'][0]
requirements = []

#iterate through sub dicts to find missing requirements marked by status:FAIL
for i in range(len(data)):
    if data[i]['status'] == 'FAIL':
        reqs = data[i]['requirements']
        for j in range(len(reqs)):
            if reqs[j]['status'] == 'FAIL':
                if 'subRequirements' in reqs[j]:
                    subreqs = reqs[j]['subRequirements']
                    for k in range(len(subreqs)):
                        if subreqs[k]['status'] == 'FAIL':
                            s = subreqs[k]['title']
                            s = s.split(' - ', 1)
                            requirements.append(s[0])

#go through the list and extract the courses
#print requirement results
courses = []
print('Degree Audit - INCOMPLETE: ')
for i in range(len(requirements)):
    s = requirements[i][0:3]
    if s.isupper():
        courses.append(requirements[i])
    print(requirements[i])

print('\nRequired Coursework:')
for i in range(len(courses)):
    print(courses[i])

time.sleep(30)