from duty_file_reader import *
from datetime import datetime
from duty_list import *
from tools.testingTool import TestingTool
import utils

class MainMenu(TestingTool):

    chores_per_day = 0  
    duties = None
    month = ''
    day = -1

    def __init__(self) -> None: 
        self.duties = load_data()  

        #Set Time Variables
        time = datetime.now()
        self.month = time.strftime("%B")
        self.day = time.day



        print(f"self.duties is type {type(self.duties)}")
        print(f"self.duties[0] is type {type(self.duties[0])}")
        #print(f" due dates here is size : { len(self.due_dates) }" )
        self.task_count = 0

        self.chores_per_day = math.ceil(self.task_count / (days_in_month() - self.day))



    def menu(self):

        try:
            choice = None
            while choice != 'q':
                #self.clear_screen()

                title = f"Cleaning Duty! Today is {self.month} {self.day}!"
                print(f"{'='*10} {title} {'='*10}")
                print("Here are your duties")
                

                i = 1
                choices = []
                for d in self.duties:
                    spacing = 0
                    if i < 10:
                        spacing = " "
                    else:
                        spacing = ""
                    if d.get_due_date() != -1:
                        print(f"{spacing}{i}) {d['NAME']} \t due {self.month} {d.get_due_date()}")
                        i += 1
                        choices.append(d)
                print()

                choice = self.getNumber('Select a item to mark as complete: ', i-1, canQuit=True)

                if choice == 'q':
                    save_data(self.duties)
                else:
                    choices[choice -1].set_done()
                
                
        except KeyboardInterrupt:
            print('\n\nExiting program...\n')


if __name__ == '__main__':
    a = MainMenu()
    a.menu()
    