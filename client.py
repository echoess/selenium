#!/bin/python 
# -*- coding:utf-8 -*- 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


'''
* 登录租户端，删除掉lb实例
* @auth:ct
* @Date: 2021/08/26
'''

def login():
    '''
    登录租户端页面
    '''
    #创建webdriver chrome实例
    global driver = webdriver.chrome.webdriver.WebDriver(executable_path='E:\驻场信息\LB重复清理-selebium\chromedriver_win32\chromedriver.exe')

    #加载运营端页面
    url = ""
    driver.get(url)
    
    #用户名和密码发送登录框中
    driver.find_element_by_xpath("//*[@class='login-form']/ul/li[1]/div/div/input").send_keys("")
    driver.find_element_by_xpath("//*[@class='login-form']/ul/li[2]/div/div/input").send_keys("")
    
    #点击登录按钮进行登录
    driver.find_element_by_xpath("//*[@id = 'loginBox']/div/div/div[1]/div[3]/input").click()
    assert "No results found." not in driver.page_source

def login_clb():

    #点击负载均衡clb 
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id = 'allProduct']/div[1]/div/div[2]/div[2]/div/a"))).click()
    
    time.sleep(7)   #页面需要加载时间，设置强制等待时间，确保页面元素都加载完成
    
  
def search_vip(i):

    #点击右侧搜索框
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id = 'clb-index']/section/section/main/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]"))).click()

    #下拉框中选择VIP
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='tea-overlay-root']/div/div/ul/li[4]"))).click()

    #输入需要查询的vip
    vip = driver.find_element_by_xpath("//*[@id='clb-index']/section/section/main/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/input")
    vip.send_keys(str(i))
    vip.send_keys(Keys.RETURN)
    
    time.sleep(2) #设置强制等待时间，避免响应太快，而找不到相关元素

def deal_lb():
    
    '''
    读重复lb的vip文件，先将每个实例的监听器删除，再删除实例
    '''

    #开始读文件中的VIP
    fi = open("VIP.txt",'r')
    
    for i in fi:
    
        print(i)
        search_vip(i)

        #当上面查询到多次记录时，处理多条记录方法
        LIST = driver.find_elements_by_xpath("//*[@id='clb-index']/section/section/main/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr")
        print(len(LIST))
        
        if len(LIST) == 1:
            #查到一个vip
            driver.find_element_by_xpath("//*[@id='clb-index']/section/section/main/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/div/p/a").click()
        else:
            #第二针情况极少暂时不作考虑
            for i in range(1,len(LIST)+1):
                driver.find_element_by_xpath("//*[@id='clb-index']/section/section/main/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[%s]/td[2]/div/p/a" %i).click()
        
        time.sleep(2)
          
        #跳转到"监听器管理"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='clb-detail']/section/section/main/div/div[2]/div/div/div[1]/div[1]/ul/li[2]/a"))).click()
        time.sleep(2)
        
        #获取http/https监听器的列表
        LI = driver.find_elements_by_xpath("//*[@id='clb-detail']/section/section/main/div/div[2]/div/div/div[3]/div/div[3]/div/div[1]/div/div/ul/li")
        print(len(LI))
        time.sleep(3)
        
        for j in range(0,len(LI)):
    
            #点击http/https对应的删除按钮，将删除"监听器"                                              
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='clb-detail']/section/section/main/div/div[2]/div/div/div[3]/div/div[3]/div/div[1]/div/div/ul/li/div/div"))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='clb-detail']/section/section/main/div/div[2]/div/div/div[3]/div/div[3]/div/div[1]/div/div/ul/li/div/div/div/button[3]"))).click()
            time.sleep(2)
    
            #点击"确认按钮"
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='tea-overlay-root']/div/div[2]/div/div[3]/div/button[1]"))).click()
            time.sleep(7)
    
        driver.back()
        time.sleep(2)
        
        search_vip(i)
        
        
        #点击entry
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='clb-index']/section/section/main/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td[12]/div/div/button"))).click()
        time.sleep(3)
    
        #点击删除
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='tea-overlay-root']/div/div[2]/div/div[3]/div/button[1]"))).click()
        time.sleep(5)
    
        #返回到主页，开始下一个实例的删除工作
        driver.get("http://console.tce.cloud.yonghui.cn/clb/index")
        time.sleep(5)
        

if __name__ == "__main__":
    
    login()
    login_clb()
    deal_lb()
