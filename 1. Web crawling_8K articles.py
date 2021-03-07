import csv
from selenium import webdriver
import json
from gne import GeneralNewsExtractor
from selenium.webdriver.chrome.options import Options
import os

# chrome_options = Options()
# chrome_options.add_argument('--headless')
drive = webdriver.Chrome(executable_path="/Users/xiaoni/Downloads/chromedriver 2")

fieldnames = ["url", "content"]

csv_file = '20200704.csv'

# if the file does not exist, then create a new file
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()


def save_data(dict_data):
    new_data = {
        "url": data[i][1],
        "content": dict_data["content"]
    }
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writerow(new_data)


def recode_success(success):
    with open('success_202007.csv', 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(success)


def recode_error(error):
    with open('error_202007.csv', 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(error)


if __name__ == '__main__':
    csv_open = open('corona_domain_url.csv', 'r')
    csv_reader = csv.reader(csv_open, delimiter=';')
    data = list(csv_reader)

    for i in range(1, len(data)):
        try:
            drive.get(data[i][1])
            drive.implicitly_wait(20)
            html = drive.page_source
            extractor = GeneralNewsExtractor()
            result = extractor.extract(html,
                                       noise_node_list=['//div[@class="comment-list"]',
                                                        '//*[@style="display:none"]',
                                                        '//div[@class="statement"]'
                                                        ])
        except Exception:
            recode_error(data[i])

        else:
            recode_success(data[i])
            print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>{data[i][1]}>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            save_data(result)

        finally:
            print('closed')

print("successful!")
input()

drive.quit()
