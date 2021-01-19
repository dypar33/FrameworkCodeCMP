from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import pyperclip
import time


def checkFile(fileName):
    global tmpCode
    try:
        f = open(fileName,'r')
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다. 파일 경로 혹은 파일명과 확장자를 확인해주세요.")
        return False
    else :
        tmpCode = f.read()
        f.close()
        return True

def getFileAddress() :
    global tmpCode
    global originCode
    global cmpCode
    while True:
        print("원본 코드 파일의 이름을 입력해주세요.(확장자까지!)")
        originCodeFile = input("==>")
        if checkFile(originFileAddress[:-1]+'\\'+originCodeFile) == True:
            break
    originCode = tmpCode
    while True:
        print("비교할 코드 파일의 이름을 입력해주세요.(확장자까지!)")
        cmpCodeFile = input("==>")
        if checkFile(cmpFileAddress+"\\"+cmpCodeFile) == True:
            break
    cmpCode = tmpCode

address = """https://wepplication.github.io/tools/compareDoc/""" #code cmp site


global tmpCode
global originCode
global cmpCode
tmpCode = ''
originCode = ''
cmpCode = ''

f = open('address_option.txt','r',encoding="UTF-8")
originFileAddress = f.readline()
cmpFileAddress = f.readline()
f.close()

print("###코드 비교 프로그램 MadeBy dypar###")
print("비교시 두페이지 옵션을 사용하시면 더 보기 편합니다.")
print("원본, 비교 대상 파일의 디렉토리 경로는 address_option.txt에서 지정해 주세요.")

print("현재 지정된 원본 파일 경로입니다. "+originFileAddress[:-1])
print("현재 지정된 비교 대상 파일의 경로입니다. "+cmpFileAddress)
print()

getFileAddress()

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance':'OFF'}
chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_experimental_option('w3c', False)
#option setting

driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options) #driver setting

sleepTime = 2
try:
    while True:
        driver.get(address)
        time.sleep(2)
        originInput = driver.find_element_by_xpath("""/html/body/main/div/form/div[2]/div[1]/textarea""")
        pyperclip.copy(originCode)
        originInput.send_keys(Keys.CONTROL,'v')

        cmpInput = driver.find_element_by_xpath("""/html/body/main/div/form/div[2]/div[2]/textarea""")
        pyperclip.copy(cmpCode)
        cmpInput.send_keys(Keys.CONTROL,'v')

        submit_btn = driver.find_element_by_xpath("""//*[@id="convertBtn"]""")
        submit_btn.click()

        print("다른 파일도 비교하겠습니까? 1 = Yes, 2 = No")
        a = input("==>")
        if a == '2':
            break
        getFileAddress()

    
except Exception as e:
    print(e)
finally:
    driver.quit()
