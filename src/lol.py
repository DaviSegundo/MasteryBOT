from riotwatcher import LolWatcher

class LoLAPI:

    def __init__(self, key) -> None:
        self.region = 'br1'
        self.lol_watcher = LolWatcher(key)
        self.latest = self.lol_watcher.data_dragon.versions_for_region(self.region)['n']['champion']
        self.champion_list = self.lol_watcher.data_dragon.champions(self.latest, False, 'pt_BR')
        
        self.dict_champions = {v['key']: k  for k,v in self.champion_list['data'].items()}

    def get_id(self, name: str, region: str = 'br1'):
        self.person = self.lol_watcher.summoner.by_name(region, name)
        self.id = self.person.get('id')
        self.puuid = self.person.get('puuid')
        self.name = self.person.get('name')
        self.level = self.person.get('summonerLevel')
        self.region = region

        return self

    def get_mastery(self):
        self.mastery_info = self.lol_watcher.champion_mastery.by_summoner(self.region, self.id)
        champions_no_chest = [c for c in self.mastery_info if c.get('chestGranted') == False]
        champions_no_chest_data = []
        for i in champions_no_chest:
            # info = {}
            # info['name'] = self.dict_champions.get(str(i.get('championId')))
            # info['mastery'] = i.get('championLevel')
            # info['points'] = i.get('championPoints')
            info = []
            info.append(self.dict_champions.get(str(i.get('championId'))))
            info.append(i.get('championLevel'))
            info.append(i.get('championPoints'))
            champions_no_chest_data.append(info)
        return champions_no_chest_data

if __name__ == '__main__':
    lol = LoLAPI().get_id('BrainLag').get_mastery()

    
