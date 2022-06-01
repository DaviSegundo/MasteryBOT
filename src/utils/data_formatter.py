from tabulate import tabulate

class Formatter:

    def __init__(self) -> None:
        pass

    def format_champions_no_chest(self, infos: list, player):
        infos.insert(0, ['Champion', 'Mastery', 'Points'])
        response = f'Name: {player.name}\nLevel: {player.level}\n\nNext champions to get chest:\n'
        response += tabulate(infos, headers="firstrow",
                            tablefmt="pretty", numalign="right")
        return response

    def format_top_mastery(self, top):
        top.insert(0, ['Champion', 'Mastery', 'Points'])
        response = ''
        response += tabulate(top, headers="firstrow",
                            tablefmt="pretty", numalign="right")
        return response

    def ranked_info(self, ranked):
        ranked.insert(0, ['Rank', 'LP', 'Wins/Loses', 'Win Rate'])
        response = ''
        response += tabulate(ranked, headers="firstrow",
                            tablefmt="pretty", numalign="right")
        return response

    def champion_info(self, champion):
        champion.insert(0, ['Champion', 'KDA Rate', 'KDA Data', 'Win Rate', 'Games'])
        response = ''
        response += tabulate(champion, headers="firstrow",
                            tablefmt="pretty", numalign="right")
        return response

    def format_clash_info(self, pi, o1, o2, o3):
        response = f"```Name:{pi[0]}\nLevel:{pi[1]}\n\nRank Information:\n{o1}\n\nTop Mastery:\n{o3}\n\nRanked Games:\n{o2}```"
        return response

    def format_name_available(self, name, level, last_game, date_cleanup, days_cleanup, months):
        response = f'```{name} is available in {days_cleanup} days.\n\nLast game: {last_game}\nIt takes {months} months for cleanup\nCleanup date (if inactive): {date_cleanup}\nCurrent Level: {level}```'
        return response
