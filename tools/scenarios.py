import utils
from .testingTool import TestingTool
import os

class ScenarioTool(TestingTool):
    def menu(self) -> None:
        choice = None
        while choice != 'q':
            print(f"{'='*10} Scenario Editor {'='*10}")

            scenarios = os.listdir('./scenarios')
            scenarios.remove('.gitkeep') # only meant to keep the folder in Git
            for i in range(len(scenarios)):
                print(f"{i + 1}. {utils.removesuffix(scenarios[i], '.bak')}")
            print()

            print('Actions: (s)ave the current database, (l)oad a scenario, (d)elete a scenario, (q)uit')
            choice = self.getLetter('What would you like to do? > ', ['s', 'l', 'd', 'q'])
            if choice == 's':
                self.enterSubmenu(self._saveScenario)
            elif choice == 'l':
                self.enterSubmenu(self._loadScenario, scenarios)
            elif choice == 'd':
                self.enterSubmenu(self._deleteScenario, scenarios)
            
            utils.clearScreen()
    

    def _saveScenario(self):
        print()
        name = self.input('What would you like to name the database backup? > ', canBeBlank=False)
        self.db.saveScenario(name)


    def _loadScenario(self, scenarios: list):
        print()
        scenario = self.getNumber('Which scenario would you like to load? > ', len(scenarios))
        scenario = scenarios[scenario - 1]
        choice = self.getLetter(f"\nYou are loading \"{scenario}\".\nYou will not be able to cancel this operation once it begins.\n\nReally load this database? (y/n) > ", ['y', 'n', 'q'])
        if choice == 'y':
            dbLoaded = False
            while not dbLoaded:
                try:
                    print('\nDatabase loading... Please wait...')
                    self.db.loadScenario(scenario)
                    dbLoaded = True
                except KeyboardInterrupt:
                    print(utils.COLORCANCEL + '\n\nLoading of database cannot be interrupted. Please wait...\n' + utils.COLORRESET)


    def _deleteScenario(self, scenarios: list):
        print()
        scenario = self.getNumber('Which scenario would you like to delete? > ', len(scenarios))
        scenario = scenarios[scenario - 1]
        os.remove(f"./scenarios/{scenario}")
