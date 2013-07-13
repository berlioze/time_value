class TimeValueMeta(type):
    units = {
        'second': 1,
        'minute': 60,
        'hour': 3600,
        'day': 86400,
        'week': 604800,
        'year': 31536000
    }
    def __getattr__(cls, time_text):
        terms = cls.parse_time(time_text)

        return cls.convert_time(terms)

    def parse_time(cls, time_text):
        if time_text != time_text.upper():
            raise ValueError("Time data should be in uppercase")

        terms = time_text.lower().split('_')
        if len(terms) < 4 or len(terms) > 5:
            raise ValueError("Time data should meet the format 'GET_[NUMBER]_XXX_IN_YYY'")

        if terms[-2] != "in":
            raise ValueError("Time data should ends with _IN_XXX")
        
        if terms[0] != "get":
            raise ValueError("Time data should starts with GET_")

        return terms

    def convert_time(cls, terms):
        unit_from = terms[-3]
        if unit_from[-1] == 's':
            unit_from = unit_from[:-1]
        unit_to = terms[-1][:-1]

        num = int(terms[1]) if len(terms) == 5 else 1

        return num * cls.units[unit_from] / cls.units[unit_to]

class TimeValue(object):
    __metaclass__ = TimeValueMeta

if __name__ == '__main__':
    assert TimeValue.GET_30_DAYS_IN_WEEKS == 4
    assert TimeValue.GET_365_DAYS_IN_YEARS == 1
    assert TimeValue.GET_YEAR_IN_DAYS == 365
    assert TimeValue.GET_DAY_IN_HOURS == 24
    assert TimeValue.GET_WEEK_IN_DAYS == 7
    print "Tests passed"
