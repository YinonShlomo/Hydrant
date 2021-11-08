import random
import xlrd
import time
import urllib.request
import datetime



# URL_FULL = "https://______"
URL_BASIC = "https://_____"


class Hydrant:
    def __init__(self, hydrant_phones, triggers, status, liter_range, bar_range):
        """this __init__ function takes the the arguments and make an object based on those arguments as attributes.
        the object is a warning (התרעה) at hydrant system.
        The warning number choose randomly by the function, as such as the liter/bar value if needed"""
        self.hydrant_phones = hydrant_phones
        self.triggers = [num.strip() for num in triggers.split(",")]
        self.status = [num.strip() for num in status.split(",")]
        self.liter_range = [int(num) for num in liter_range.split(",")]
        self.bar_range = [int(num) for num in bar_range.split(",")]

        self.current_hydrant_phone = random.choice(hydrant_phones)
        self.current_trigger = random.choice(self.triggers)
        self.current_status = random.choice(self.status)
        self.current_liter = random.randrange(self.liter_range[0], self.liter_range[1])
        self.current_bar = random.randrange(self.bar_range[0], self.bar_range[1])
        self.value = 0

        if self.current_trigger in ["1", "2", "7"]:
            self.current_status = "0"
            if self.current_trigger in ["1", "2"]:
                self.value = self.current_liter
            else:
                self.value = self.current_bar
        else:
            self.current_status = "1"

    def __str__(self):
        """this function print the object attributes"""
        return f"hydrant = {self.current_hydrant_phone}, trigger = {self.current_trigger}, value = {self.value}, status = {self.current_status}"

    def set_hydrant_phone(self, phone):
        self.current_hydrant_phone = phone

    def set_trigger(self, trigger):
        self.current_trigger = trigger

    def set_status(self, status):
        self.current_status = status

    def set_value(self, value):
        self.value = value

    def create_url(self):
        """this function takes objects attributes and make a url for sending to hydrants system"""
        return f"{URL_BASIC}{self.current_hydrant_phone}/T/{self.current_trigger}/V/{self.value}/S/{self.current_status}"

    def event_continuation(self):
        """this function create existing object and change its value attribute.
        value attribute represents liters on flow or bar on pressure """
        #if self.current_status == "0":
        #    time.sleep(1)
        if self.current_trigger in ["1", "2"]:
            Hydrant.set_value(self, random.randrange(self.liter_range[0], self.liter_range[1]))
            #self.value = random.randrange(self.liter_range[0], self.liter_range[1])
        else:
            Hydrant.set_value(self, random.randrange(self.bar_range[0], self.bar_range[1]))
            #self.value = random.randrange(self.bar_range[0], self.bar_range[1])

    def end_event(self):
        """this function ends an event, by changing its status to 1"""
        self.event_continuation()
        self.current_status = "1"

    def send_url(self):
        """this function get url, and send it to the website of hydrants which send it the the DB"""
        response = urllib.request.urlopen(self.create_url())
        html = response.read()
        file = open(r"...\log.txt", "w")
        file.write(f"{datetime.datetime.now()}\n{html}\n\n")
        if html == b'{"responeStatus":0,"responeTitle":"OK","responeMsg":"Parameters successfully updated!"}':
            print("Event Sent Successfully")
        else:
            print("Error. Message Did NOT Send")


def reading_files():
    """this function read a file which contain variables (triggers, status, liter and bar ranges) and decompose it to
    seprated values for the next stage - Hydrant.__init__ """
    with open(r"...\lists.txt", "r") as file:
        reading = file.readlines()
        for line in reading:
            split = line.strip().split(":")
            if split[0] == "triggers":
                global triggers
                triggers = split[1]
            elif split[0] == "status":
                global status
                status = split[1]
            elif split[0] == "liters_range":
                global liter_range
                liter_range = split[1]
            elif split[0] == "bars_range":
                global bar_range
                bar_range = split[1]

    file = r"...\hydrants_phones.xls"
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    global hydrant_phones
    hydrant_phones = [sheet.cell_value(i, 0) for i in range(sheet.nrows)]


def welcome():
    print("Welcom to Hydrants' Keepie Simulator System\n")
    choice = int(input("For create a warning manually, press 1\nFor create warning automatically & randomly, press 2\n"))
    return choice


def manually_warning():
    """"in this function the user select manually the warning(התרעה)"""
    print("In this simulator you will create a warning (התרעה) and its attributes manually.\n")
    warning = input("Please select warning(התרעה):\nWater flow - 1\nReverse water flow - 2\nVandalism - 3\nLow battery - 5\nLife signal - 6\nPressure state - 7\n")
    return warning


def manually_hydrant():
    """"in this function the user select manually the hydrant"""
    print("Please select hydrant phone")
    str = ""
    for hydrant, num in zip(hydrant_phones, range(1, len(hydrant_phones) +1)):
        str += f"Press {num} for hydrant number {hydrant}\n"
    num = input(str)
    return hydrant_phones[int(num)-1]


def manually_value(warning):
    """"in this function the user select manually the value for warning 1,2 and 7.
    In other warnings, the system automaticly select 0 """
    print("Please select value for the warning(התרעה), for warning 1,2 or 7")
    if warning in ["1", "2"]:
        return input("Select number of litters for flow\n")
    elif warning == "7":
        return input("Select number of bar for pressure\n")
    else:
        return "0"


def manually_status(warning):
    print("Please select status of the warning(התרעה), for warning 1,2 or 7")
    if warning in ["1", "2", "7"]:
        return input("for opening warning - press 0,\nfor closing warning - press 1\n")
    else:
        return "1"


def create_events(num = int):
    for i in range(num + 1):
        i = Hydrant(hydrant_phones, triggers, status, liter_range, bar_range)
        print(i)
        time.sleep(4)
        print(Hydrant.event_continuation(i))




welcome = welcome()
reading_files()
if welcome == 1: #ידני
    b = Hydrant(hydrant_phones, triggers, status, liter_range, bar_range)
    warning = manually_warning()
    Hydrant.set_trigger(b, warning)
    manually_value = manually_value(warning)
    Hydrant.set_value(b, manually_value)
    manually_status = manually_status(warning)
    Hydrant.set_status(b, manually_status)
    hydrant = manually_hydrant()
    Hydrant.set_hydrant_phone(b, hydrant)
    print(f"b = {b}")
    Hydrant.send_url(b)

elif welcome == 2:
    a = Hydrant(hydrant_phones, triggers, status, liter_range, bar_range)
    Hydrant.send_url(a)
    print(a)
    if a.current_trigger in ["1", "2", "7"]:
        time.sleep(10)
        Hydrant.event_continuation(a)
        Hydrant.send_url(a)
        print(a)
        time.sleep(10)
        Hydrant.end_event(a)
        print(a)
        Hydrant.send_url(a)


