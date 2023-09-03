from config.models import BaseDatesModel


class Country(BaseDatesModel):
    class Meta:
        db_table = 'Country'
