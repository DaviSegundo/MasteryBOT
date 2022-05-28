from riotwatcher import LolWatcher


class LoLAPI:

    def __init__(self, key) -> None:
        self.region = 'br1'
        self.lol_watcher = LolWatcher(key)
        self.get_champions_list()

    def get_informations_by_name(self, name: str, region: str = 'br1'):
        self.person = self.lol_watcher.summoner.by_name(region, name)
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
