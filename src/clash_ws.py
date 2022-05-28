from urllib import request
from bs4 import BeautifulSoup


class ClashWebScrap:

    def __init__(self, name) -> None:
        self.url = f'https://br.op.gg/summoners/br/{name.lower()}'

    def get_html_from_site(self):
        resp = request.urlopen(self.url)
        html = resp.read().decode("utf8")
        self.soup = BeautifulSoup(html, 'html.parser')
        
    def get_elo_info(self):
        elos = self.soup.find_all('div', class_='tier')
        lps = self.soup.find_all('div', class_='lp')
        wrs = self.soup.find_all('div', class_='win-lose')

        self.ranked = []
        for elo, lp, wr in zip(elos, lps, wrs):
            infos = []
            infos.append(elo.text)
            infos.append(lp.text)
            infos.append(wr.text[:-12])
            infos.append(wr.text[-12:])
            self.ranked.append(infos)
    
    def get_champions_ranked(self):
        champions = self.soup.find_all('div', class_='champion-box')
        self.champions_infos = []
        for champion in champions:
            info = []
            info.append(champion.find('div', class_='name').text)
            kda_info = champion.find('div', class_='kda').text.replace(' ', '').split('KDA')
            info.append(kda_info[0][:-2])
            info.append(kda_info[1])
            info.append(champion.find('div', class_='played').find('div', attrs={'style': 'position:relative'}).text)
            info.append(champion.find('div', class_='played').find('div', attrs={'class': 'count'}).text[:-7])
            self.champions_infos.append(info)

    def run(self):
        self.get_html_from_site()
        self.get_elo_info()
        self.get_champions_ranked()

        return self

if __name__ == '__main__':
    ws = ClashWebScrap('TheAcclaimed').run()
    print(ws)
    