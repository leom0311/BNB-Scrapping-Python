import requests
from bs4 import BeautifulSoup
import csv
import time

# Define the URL to scrape
url = 'https://bscscan.com/txs?p=1'

import subprocess

n = 0
with open('transactions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Transaction Hash', 'Result', 'Method', 'Block', 'Timestamp', 'From', 'To', 'Value', 'Txn Fee'])
    while(True):
        n = n + 1
        print("get data from server: ", n)
        # Run the curl command
        result = subprocess.run(['curl', '-s', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

        # Check the result
        if result.returncode == 0:
            html = result.stdout
            soup = BeautifulSoup(html, 'html.parser')
            trs = soup.find_all('tr')
            for tr in trs:
                tag = tr.find('a', class_='myFnExpandBox_searchVal')
                if tag is None:
                    continue
                tds = tr.find_all('td')
                if len(tds) != 13:
                    continue

                # Transaction Hash
                hash = tds[1].find('a', class_="myFnExpandBox_searchVal").get_text()
                
                result = "Fail"
                if tds[1].find(class_='fa-exclamation-circle') is None:
                    result = "Success"
                else:
                    continue

                # Method 
                method = tds[2].find('span').get_text()

                # Block
                block = tds[3].find('a').get_text()

                # date
                date = tds[4].find('span').get_text()

                # Age
                # print(tds[5].find('span').get_text())

                # From
                from_ = tds[7].find('span')
                if from_ is None:
                    from_ = tds[7].find('a').get_text()
                else:
                    from_ = tds[7].find('span').get('data-highlight-target')
                
                # To
                to_ = tds[9].find('span')
                if to_ is None:
                    to_ = tds[9].find('a').get_text()
                else:
                    to_ = tds[9].find('span').get('data-highlight-target')

                # Value
                value = tds[10].find('span').get_text()

                # Txn Fee
                fee = tds[11].get_text()
                hash        = "" if hash is None else hash
                result      = "" if result is None else result
                method      = "" if method is None else method
                block       = "" if block is None else block
                date        = "" if date is None else date
                from_       = "" if from_ is None else from_
                to_     = "" if to_ is None else to_
                value       = "" if value is None else value
                fee     = "" if fee is None else fee
                writer.writerow([hash.strip(), result.strip(), method.strip(), block.strip(), date.strip(), from_.strip(), to_.strip(), value.strip(), fee.strip()])
        else:
            print(f"Failed to retrieve data. Error: {result.stderr}")
        time.sleep(3)
