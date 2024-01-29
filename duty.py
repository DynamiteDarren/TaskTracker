from datetime import datetime
import math

def days_in_month():
    month = datetime.now().month
    days = 31
    if (month in [4,6,9,11]):
        days = 30
    elif month == 2:
        days = 28
    return days

class Duty(dict):

    due_date = -1
    index = None
    
    def __init__(self, mapping=None, /, **kwargs):
        if mapping is not None:
            mapping = {
                str(key).upper(): value for key, value in mapping.items()
            }
        else:
            mapping = {}
        if kwargs:
            mapping.update(
                {str(key).upper(): value for key, value in kwargs.items()}
            )
        super().__init__(mapping)

        self.due_date = self._calculate_due_date()



    def __setitem__(self, key, value):
        key = key.upper()
        super().__setitem__(key, value)

    def get_name(self):
        return self.name

    def _calculate_due_date(self):
        print("here in get due date")
        frequency =  days_in_month() / int(self["FREQUENCY"])
        due_date = -1
        counter = -1
        
        while (due_date < datetime.now().day):
            due_date += frequency
            counter += 1
        self.index = -(int(self["FREQUENCY"]) - counter)
    
        if self["DATA"] == '':
            self["Data"] = '0' * int(self["FREQUENCY"])
            print(f"New data {self['DATA']}")

        if len(self["DATA"]) >= self.index and self["DATA"][self.index] == '1':
            print("HERE?")
            return -1
        else:
            print("oh")
            return math.floor(due_date)
        
    def get_due_date(self):
        return self.due_date
    
    def set_done(self):
        a = list(self["DATA"])
        #print(self["DATA"])
        a[self.index] = '1'
        self["DATA"] = ''.join(a)
        #print(self["DATA"])
        self.due_date = -1
        


