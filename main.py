import requests
import re
import os
import urllib.parse as ulp
from bs4 import BeautifulSoup
import shutil
import pathlib




target_url = "http://riweb.tibeica.com/crawl/"
target_links = []

def cfhtml(name):
    response = requests.get(name)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    body = soup.find('body')

    if name[-5:] == ".html":
        name2 = os.path.basename(name)
        ye = os.path.splitext(name2)
        folder_name = ye[0]

        save_path = r'C:\Users\Catalin\Desktop\Proiect Riw\Partea 2\data\crawl'
        name_of_file = name2
        x = os.path.join(save_path, folder_name)
        if os.path.exists(x):
            shutil.rmtree(x)
        os.makedirs(x)

        completeName = os.path.join(x, name_of_file)
        f = open(completeName, "w")
        f.write(str(body))

def createDir(url):
    response = requests.get(url)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    body = soup.find('body')
    if url != 'http://riweb.tibeica.com/crawl/':
        name2 = os.path.basename(url)
        url_array = url.split('/')
        path = ""
        for value in url_array[2:]:
            if path == "":
                path += value
            else:
                path += "\\" + value
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            if value[-5:] == ".html":
                value= "_" + value
                completeName = os.path.join(path, value)
                f = open(completeName, "w")
                f.write(str(text))

        return path

def extract_links_from(url):
    print(url)
    response = requests.get(target_url)
    createDir(url)
    return re.findall('(?:href=")(.*?)"', response.content.decode('ISO-8859-1'))


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = ulp.urljoin(target_url, link)
        if "#" in link:
            link = link.split("#")[0]
        if target_url in link and link not in target_links:
            target_links.append(link)
            crawl(link)


crawl(target_url)























