from bs4 import BeautifulSoup
import requests
import crayons
import concurrent.futures
import os

links = [
    "https://papers.gceguide.com/A%20Levels/Mathematics%20(9709)/", "https://papers.gceguide.com/A%20Levels/Physics%20(9702)/",
    "https://papers.gceguide.com/A%20Levels/Computer%20Science%20(for%20final%20examination%20in%202021)%20(9608)/",
    "https://papers.gceguide.com/A%20Levels/Chemistry%20(9701)/"
]

print(crayons.yellow("[!] links read complete !"))

print(crayons.yellow("[!] Getting HTML from pages !"))
req_texts = [requests.get(txt).text for txt in links]
print(crayons.green("[!] Got HTML from pages !"))

print(crayons.yellow("[!] Parsing HTML from pages !"))
soups = [BeautifulSoup(txt, "lxml") for txt in req_texts]
print(crayons.yellow("[!] Parsed HTML from pages !"))


def download_data(link, id):
    print(crayons.yellow("[!] Starting Download !"))
    req = requests.get(links[id] + link).content

    _dir = links[id].split("/")[-2].replace("%20", "")

    if not os.path.isdir(_dir):
        print(crayons.yellow("[!] Creating Directory !"))
        os.mkdir(_dir)

    with open(f"{_dir}\\{link}", "wb") as pdf_data:
        print(crayons.yellow("[!] Writing to file !"))
        pdf_data.write(req)
        print(crayons.green(f"[+] '{link}' Downloaded for {link} !"))
        print(crayons.yellow(f"[!] from '{links[i]}{link}'"))


i = 0
threads = []
for soup in soups:
    print(crayons.yellow("[!] Parsing href from a tag !"))
    link_obj = soup.select("tr td a")
    for d in link_obj:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            _dir = links[i].split("/")[-2].replace("%20", "")
            if os.path.isfile(f"{_dir}\\{d.get('href')}"):
                print(crayons.red(f"[!] file {_dir}\\{d.get('href')} already downloaded !"))
                continue

            print(crayons.yellow("[!] Adding to thread list !"))
            temp = executor.submit(download_data, d.get("href"), i)
            print(crayons.yellow("[!] Added to thread list !"))
            threads.append(temp)
    # download_data(d.get("href"), i)

    i += 1

for thread in concurrent.futures.as_completed(threads):
    print(crayons.yellow("[!] Waiting for all to complete !"))
    print(thread.result())
