import datetime as dt


def year(request):
    """
    Добавляет переменную с текущим годом.
    """
    now = dt.datetime.now()
    year = now.year
    return {
        "year": year
    }