import os
from dotenv import load_dotenv
from deta import Deta


load_dotenv(".env")
DATA_NAME = "TQbJzbUE"
#DATA_KEY = "TQbJzbUE_VXkxWZgggZfvmCXVsGdriKcscrmfvHCU"
DATA_KEY = os.getenv("b0gzhyby2bg_WKXqhgr66gmZVUKRoeN8dtjjef4i2uMw")

deta = Deta(DATA_KEY)

db = deta.Base("Monthly_Reports")

def insert_period(period, incomes, expences, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "incomes": incomes, "expenses": expences, "comment": comment})


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)
