from datetime import datetime
import math
from duty import Duty


total_duties = 0

class  duty_list(list):

    def __init__(self, iterable):
        super().__init__(Duty(item) for item in iterable)

    def __setitem__(self, index, item):
        super().__setitem__(index, Duty(item))

    def insert(self, index, item):
        super().insert(index, Duty(item))

    def append(self, item):
        super().append(Duty(item))

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(Duty(item) for item in other)

    def get_due_dates(self):
        due_dates = []
        print(f"Tasks is type {type(self)}")
        for task in self:
            print(f"Task is type {type(task)}: {task}")
            due_date = task.get_due_date()
            print("HERE!")
            if due_date != None:
                due_dates.append(due_date)
        print(f"Here the size is {len(due_dates)}")
        return due_dates

    def toString(self):
        string = "["

        

def days_in_month():
    month = datetime.now().month
    days = 31
    if (month in [4,6,9,11]):
        days = 30
    elif month == 2:
        days = 28
    return days

def sort_by_due_date():
    return 0

def get_index_for_data(count):
    frequency =  days_in_month() / count
    due_date = 0
    counter = -1
    while (due_date < datetime.now().day):
        due_date += frequency
        counter += 1
    index = count - counter




