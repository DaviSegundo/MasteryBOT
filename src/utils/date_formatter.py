from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class DateFormatter:

    def __init__(self) -> None:
        pass

    def format_loldate(self, game_creation):
        formated_timestamp = int(str(game_creation)[:-3])
        date = datetime.fromtimestamp(formated_timestamp)
        return date

    def format_date_gamecreation(self, game_creation):
        date = self.format_loldate(game_creation)
        date = date.strftime("%d %b %Y - %H:%M:%S")
        return date

    def format_date_cleanup(self, game_creation, level):
        if level <= 6:
            months = 6
        else:
            months = 6 + (level - 6)
            if months > 30:
                months = 30
        
        date = self.format_loldate(game_creation)
        
        date_cleanup = date + relativedelta(months=months)
        date_cleanup_formated = date_cleanup.strftime("%d %b %Y")

        days_cleanup = (date_cleanup - date).days
        
        return date_cleanup_formated, days_cleanup, months
        
