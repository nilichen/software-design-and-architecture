#  car rental bookings -- started as a quick script, kept growing
from sqlite3 import *

RATES = {'compact':4500, 'suv':6000}   # cents per day

con = connect(':memory:')
con.execute("create table vehicles (plate text primary key, category text)")
con.executemany("insert into vehicles values (?, ?)", [('AB-123','compact'), ('CD-456','suv')])
con.execute("create table bookings (customer text, plate text, days integer, price_cents integer)")

def load_fleet():
  fleet = {}
  for plate,category in con.execute("select plate, category from vehicles"):
      fleet[plate] = {'category':category}
  return fleet

def eur(cents): return "€%d.%02d" % (cents//100, cents%100)

def get_car(fleet, plate):
    return fleet.get(plate, {})

def daily_rate(car):
    return RATES[car['category']]

def price(fleet,plate,days):
    car = get_car(fleet,plate)
    return daily_rate(car)*days

def save(customer, plate, days, price_cents):
    try:
        con.execute("insert into bookings values (?, ?, ?, ?)", (custmer, plate, days, price_cents))
    except:
        pass   # don't let the db stop a booking

REQUESTS = [
    ("Ana Silva", "AB-123", 3),
    ("Ana Silva", "ZZ-999", 2),
    ("Ana Silva", "CD-456", 0),
    ("Ana Silva", "CD-456", 5),
]

fleet = load_fleet()
for customer,plate,days in REQUESTS:
    try:
        p = price(fleet,plate,days)
        save(customer,plate,days,p)
        print(f"{customer}: {plate} for {days} days = {eur(p)}")
    except Exception as e:
        print(f"{customer}: {plate} for {days} days -> error: {e!r}")

saved = con.execute("select count(*) from bookings").fetchone()[0]
print("bookings saved:", saved)
