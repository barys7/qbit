from bs4 import BeautifulSoup
import requests
import os
from download import Download
import sys

class Tdownloader:
    def __init__(self, title):
        self.title = title.replace(' ', '+')
        self.pg = 1

    def get_title(self):
        return self.title

    def Contents(self, url):
        headers = {
            'user-Agent': 'Mozilla/5.0'
        }
        with requests.get(url, headers=headers) as data:
            contents = BeautifulSoup(data.content, "html.parser")
        return contents

    def Informations(self, page=1):
        """
            Get information from https://1337x.to/
        """
        numbers_list = []
        urls_list = []
        names_list = []
        seeds_list = []
        leeches_list = []
        sizes_list = []
        informations = []

        contents = self.Contents(f"https://1337x.to/search/{self.title}/{page}/")
        urls = contents.findAll("td", "name")
        names = contents.findAll("td", "name")
        seeds = contents.findAll("td", "seeds")
        leeches = contents.findAll("td", "leeches")
        sizes = contents.findAll("td", "size")

        [numbers_list.append(count) for count in range(1, len(names))]
        [names_list.append(name.a.next_sibling.text.strip(' ⭐'))
         for name in names]
        [seeds_list.append(seed.text) for seed in seeds]
        [leeches_list.append(leech.text) for leech in leeches]
        [sizes_list.append(size(text=True, recursive=False)[0])
         for size in sizes]
        [urls_list.append(url.a.next_sibling["href"]) for url in urls]

        [informations.append(info) for info in zip(
            numbers_list, names_list, seeds_list, leeches_list, sizes_list, urls_list)]

        return informations

    def ShowInfo(self, page=1):
        BOLD = '\033[1m'
        CGREY = '\33[90m'
        OKBLUE = '\033[94m'
        WARNING = '\033[93m'
        GREEN = '\33[32m'
        RED = '\033[91m'
        ENDC = '\033[0m'

        print(f"\n{WARNING}NUMBER{ENDC}\t\t{BOLD}NAME{ENDC}\t\t{GREEN}SEEDS{ENDC}\t\t{RED}LEECHES{ENDC}\t\t{OKBLUE}SIZE{ENDC}")
        print(f'{CGREY}={ENDC}' * 90)

        for i in self.Informations(page=page):
            print(
                f"{WARNING}{i[0]}{ENDC} | {BOLD}{i[1]}{ENDC} |{GREEN}{i[2]}{ENDC} | {RED}{i[3]}{ENDC} |{OKBLUE}{i[4]}{ENDC}",
                end='\n{}{}{}\n'.format(CGREY, '=' * 90, ENDC)
            )
        print(f"{BOLD} PAGE {page} {ENDC}\n")

    def GetPath(self):
        path = os.path.abspath(__file__)
        base_dir = os.path.dirname(path)
        download_path = os.path.join(base_dir, 'downloads')
        os.makedirs(download_path, exist_ok=True)
        return download_path

    def next_page(self):
        os.system("clear")
        self.pg += 1
        self.ShowInfo(self.pg)
        self.select_page()
        return self.pg

    def prev_page(self):
        os.system("clear")
        self.pg -= 1
        self.ShowInfo(self.pg)
        self.select_page()
        return self.pg

    def select_page(self):
        ch = input("[?] 'next' for next page\n[?] 'prev' for previous page\n[?] 'ok' stay right page:  ")
    
        if ch == str("next"):
            mpage = self.next_page()
        elif ch == str("prev"):
            if self.pg == 1:
                raise TypeError("this page is 1 .. not previous page exist !!!!!")
            mpage = self.prev_page()
        elif ch == str("ok"):
            mpage = self.pg
        else:
            raise TypeError("bad choice")

    def Download_Torrent_File(self):
        choose = int(input("select number: "))
        for i in self.Informations(page=self.pg):
            if choose == int(i[0]):
                os.system("clear")
                print(f"[+] {i[1]}")
                print(f"[+] getting magnet")
                content = self.Contents(f'https://1337x.to{i[5]}')
                magnet_link = content.find("div", "no-top-radius").a["href"]
                Download(magnet_link)
                print("\n\t download started .. \n")

def main():       
    inp = str(input("search: "))
    a = Tdownloader(inp)
    print(f"you search for '{a.get_title()}'\n")
    a.ShowInfo()
    a.select_page()
    a.Download_Torrent_File()

if __name__ == '__main__':
    main()
    while True:
        again = input("do you want to search again?(y or n): ")
        if again == str('y'):
            main()
        elif again == str('n'):
            sys.exit()
        else:
            raise TypeError("bad choice")
            sys.exit()
