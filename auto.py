from selenium import webdriver
from configparser import ConfigParser
import time
import datetime
def valid_user():
    # 20180730 10:03기준 6시간
    print(time.time())
    now = 1534658874.3394372
    terminTime = now + 60 * 60 * 3
    print("체험판 만료기간 : ", time.ctime(terminTime))
    if time.time() > terminTime:
        print('만료되었습니다.')
        exit(-1)

# === CONFIG 부분
config = ConfigParser()
config.read('CONFIG.ini',encoding='utf8')  # INI 읽어오기
ID = config.get('USER', 'ID')
PW = config.get('USER', 'PW')
TW_CONTENT = config.get('TWEET', 'CONTENT')
TW_PIC = config.get('TWEET', 'PIC')
TW_TIMELIST = config.get('TWEET', 'TIMELSIT').split(',')
# ===============
def how_many_sleep(_idx):
    kor_time = datetime.datetime.now()
    target_time = datetime.datetime.strptime(TW_TIMELIST[_idx], "%H:%M")
    time_diff = target_time - kor_time
    #print('>>> {}분 후에 시작합니다.'.format(int(time_diff.seconds / 60)))
    return time_diff.seconds


# init
driver = webdriver.Chrome('./chromedriver.exe')
driver.maximize_window()
driver.get('https://twitter.com/login')
time.sleep(3)
driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').send_keys(ID)
driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').send_keys(PW+'\n')
time.sleep(5)
# upload
idx = 0
while True:
    valid_user()
    driver.find_element_by_xpath('//*[@id="global-new-tweet-button"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="Tweetstorm-tweet-box-0"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]').send_keys(TW_CONTENT)
    file_input = driver.find_element_by_xpath('//*[@id="Tweetstorm-tweet-box-0"]/div[2]/div[2]/div[1]/span[1]/div/div/label/input')
    file_input.send_keys(TW_PIC)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="Tweetstorm-tweet-box-0"]/div[2]/div[2]/div[2]/span/button[2]').click()
    print(">>> 글을 올렸습니다.")
    time.sleep(5)
    driver.get('https://twitter.com/')
    while True:
        if int(how_many_sleep(idx))/60 > 1000:
            idx += 1
            if len(TW_TIMELIST) <= idx:
                idx = 0
        else:
            break
    delay = int(how_many_sleep(idx))
    print('>>> {}분 후에 다시 시작합니다. (예상 업로드 : {})'.format(int(delay / 60), TW_TIMELIST[idx]))
    time.sleep(delay)
    idx += 1
    if len(TW_TIMELIST) <= idx:
        idx = 0
