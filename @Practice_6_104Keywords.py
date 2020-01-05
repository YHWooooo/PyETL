import requests
from bs4 import BeautifulSoup as BS
import os, csv

path = './104keywords_job'
if not os.path.exists(path):
    os.mkdir(path)


# 檔案欄位建立

col = ['職缺名稱', '公司', '薪資', '擅長工具', '條件技能', '聯絡人']
with open('./104_config/104_columns.csv', 'w', encoding='utf-8') as f:
    col_text = str(col).replace('[', '').replace(']', '').replace('\'', '')
    f.write(col_text + '\n')
print('OK')


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

for p in range(1, 11):

    page_url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=MySQL&order=15&asc=0&page={:d}&mode=s&jobsource=2018indexpoc'.format(p)
    resp = requests.get(page_url, headers=headers)
    #print(resp.text)

    soup = BS(resp.text, 'html.parser')
    #print(soup.select('a[class="js-job-link"]'))

    # 撈取每個職缺的網址
    #print(soup.select('a[class="js-job-link"]'))
    #print(soup.select('a[class="js-job-link"]')[0])
    #print('https:' + soup.select('a[class="js-job-link"]')[0]['href'])

    # for_len 為每個頁面的職缺數量
    for_len = soup.select('a[class="js-job-link"]')
    #print(len(job_url))

    job_vac = []


    # 每次迴圈長度都是跟著職缺數跑(e.g. 第一頁職缺23、第二頁職缺20)
    for i in range(len(for_len)):

        job_url = 'https:' + soup.select('a[class="js-job-link"]')[i]['href']
        job_resp = requests.get(job_url, headers=headers)
        job_soup = BS(job_resp.text, 'html.parser')

        #print(i + 1)
        #print(job_url)

        str_job = []

        #在每個職缺頁面內 (job_url requests) 定位所需標籤
        job_title = job_soup.select('div[class="center"] h1')[0].text.strip().split('\n')[0].rstrip()
        #print(job_title)
        job_title += '@'
        #job_vac.append(job_title)

        job_company = job_soup.select('div[class="center"] h1')[0].text.strip().split('\n')[1].rstrip()
        #print(job_company)
        #job_vac.append(job_company)

        job_salary = job_soup.select('dd[class="salary"]')[0].text.split('\n')[0].replace(' ', '')
        #print(job_salary)
        job_salary += '*'
        #job_vac.append(job_salary)

        job_skill = job_soup.select('dd[class="tool"]')[0].text
        #print(job_skill)
        #job_vac.append(job_skill)

        job_demand = job_soup.select('dd[class="tool"]')[1].text
        #print(job_demand)
        #job_vac.append(job_demand)

        job_contact = job_soup.select('section[class="info"] div[class="content"]')[-1].text.lstrip().rstrip().replace('\n', ' ').replace('： ', ':')
        #print(job_contact)
        #job_vac.append(job_contact)

        str_job += job_title.split('@')[:-1]
        str_job += job_company.split(',')
        str_job += job_salary.split('*')[:-1]
        str_job += job_skill.split(',')
        str_job += job_demand.split(',')
        str_job += job_contact.split(',')

        job_vac.append(str_job)

    print(job_vac)


    with open('./104_config/104_columns.csv', 'a', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        writer.writerows(job_vac)
    print('OK')







