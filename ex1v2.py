import time
import csv
from selenium import webdriver

browser = webdriver.Chrome(executable_path="E:\Thecon\chromedriver_win32\chromedriver.exe")

browser.get("https://www.binance.com/en/trade/ETH_BUSD")
time.sleep(1)

fileVariable = open('example.csv', 'r+')
fileVariable.truncate(0)
fileVariable.close()

def write_csv(data):
    with open('example.csv', 'a+', newline='') as outfile:
        #writer = csv.writer(outfile,quoting=csv.QUOTE_NONNUMERIC,delimiter=",")
        writer = csv.writer(outfile,delimiter=",")
        writer.writerow([data])

#
# def open_csv(filename):
#     with open(filename, "r+") as f:
#         text = f.read()
#         f.seek(0)  # return to the top of the file
#         text = f.read()
#

i=0
while True:
    post_elems = browser.find_elements_by_class_name("contractPrice")
    for post in post_elems:
        print(post.text)
        i=i+1
        write_csv(post.text)
        if(i==100):
            print("Au fost scrise 100 de linii")
            exit(0)
        #time.sleep(1)

    time.sleep(1)

