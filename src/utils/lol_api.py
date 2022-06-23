from riotwatcher import LolWatcher
from requests.exceptions import HTTPError

from utils.date_formatter import DateFormatter

class LoLAPI:

    def __init__(self, key) -> None:
        self.region = 'br1'
        self.lol_watcher = LolWatcher(key)
        self.get_champions_list()

    def get_informations_by_name(self, name: str, region: str = 'br1'):
        try:
            self.person = self.lol_watcher.summoner.by_name(region, name)
        except HTTPError:
            return None
        self.id = self.person.get('id')
        self.puuid = self.person.get('puuid')
        self.name = self.person.get('name')
        self.level = self.person.get('summonerLevel')
        self.region = region

        return self

    def get_champions_list(self):
        self.latest = self.lol_watcher.data_dragon.versions_for_region(self.region)[
            'n']['champion']
        self.champion_list = self.lol_watcher.data_dragon.champions(
            self.latest, False, 'pt_BR')
        self.dict_champions = {v['key']: k for k,
                               v in self.champion_list['data'].items()}
        self.champions_dict = {k: v['key'] for k,
                               v in self.champion_list['data'].items()}

    def get_mastery_info(self):
        self.mastery_info = self.lol_watcher.champion_mastery.by_summoner(
            self.region, self.id)

    def get_top_mastery(self):
        self.get_mastery_info()

        champions_top_mastery = []
        for i in self.mastery_info:
            info = []
            info.append(self.dict_champions.get(str(i.get('championId'))))
            info.append(i.get('championLevel'))
            info.append(i.get('championPoints'))
            champions_top_mastery.append(info)
        return champions_top_mastery

    def get_no_chest(self):
        self.get_mastery_info()
        champions_no_chest = [
            c for c in self.mastery_info if c.get('chestGranted') == False
        ]

        champions_no_chest_data = []
        for i in champions_no_chest:
            info = []
            info.append(self.dict_champions.get(str(i.get('championId'))))
            info.append(i.get('championLevel'))
            info.append(i.get('championPoints'))
            champions_no_chest_data.append(info)
        return champions_no_chest_data

    def get_list_matches(self):
        self.matches = self.lol_watcher.match.matchlist_by_puuid(self.region, self.puuid)
        return self.matches

    def get_date_from_last_match(self):
        self.get_list_matches()
        last_match = self.matches[0]
        all_data = self.lol_watcher.match.by_id(self.region, last_match)
        info = all_data.get('info')
        self.game_creation = info.get('gameCreation')
        return self.game_creation

    def get_info_cleanup_date(self):
        self.get_date_from_last_match()
        formated_date = DateFormatter().format_date_gamecreation(self.game_creation)
        date_cleanup, days_cleanup, months = DateFormatter().format_date_cleanup(self.game_creation, self.level)
        
        return formated_date, date_cleanup, days_cleanup, months

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    LOL_API_KEY = os.getenv('LOL_API_KEY')
    lol = LoLAPI(LOL_API_KEY)

    player = lol.get_informations_by_name("TheAcclaimed")
    
    print(player.get_info_cleanup_date())
    