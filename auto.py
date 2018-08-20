#-*-encoding:utf8-*-
from selenium import webdriver
import time
# === CONFIG 부분

lines = open('CONFIG.txt',encoding='utf8').readlines()  # INI 읽어오기
ID = lines[1].split('::')[1].strip()
PW = lines[2].split('::')[1].strip()
TW_CONTENT = open(lines[4].split('::')[1].strip(),'r',encoding='utf-8').read()
TW_PIC = lines[5].split('::')[1].strip()
TW_TIMEDELAY = int(lines[6].split('::')[1].strip())
# ===============
# init
driver = webdriver.Chrome('./chromedriver.exe')
driver.maximize_window()
driver.get('https://twitter.com/login')
time.sleep(3)
driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').send_keys(ID)
driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').send_keys(PW+'\n')
time.sleep(5)
# upload
idx = 1
while True:
    driver.find_element_by_xpath('//*[@id="global-new-tweet-button"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="Tweetstorm-tweet-box-0"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]').send_keys(TW_CONTENT)
    file_input = driver.find_element_by_xpath('//*[@id="Tweetstorm-tweet-box-0"]/div[2]/div[2]/div[1]/span[1]/div/div/label/input')
    file_input.send_keys(TW_PIC)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="Tweetstorm-tweet-box-0"]/div[2]/div[2]/div[2]/span/button[2]').click()
    print(">>> {}번째 글을 올렸습니다.".format(idx))
    time.sleep(5)
    driver.get('https://twitter.com/')

    print('>>> {}분 후에 다시 업로드 합니다.'.format(TW_TIMEDELAY))
    time.sleep(TW_TIMEDELAY*60)
    idx += 1
