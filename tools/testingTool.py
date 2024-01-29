import utils
from typing import Callable

class TestingTool:

    
    def clear_screen(self):
        print('\033c', end='')

    def _isLetterInChoices(self, letter: str, choices: list, caseSensitive = False) -> bool:
        # If case insensitive (which is the default), make everything lowercase
        if not caseSensitive:
            choices = [c.lower() for c in choices]
            letter = letter.lower()
        
        return letter in choices
    

    def _isNumberInRange(self, n: str, max: int, min = 1) -> bool:
        # Negative and positive number signs don't affect whether it's a number
        if n.lstrip('-+').isdigit():
            n = int(n)
            return n >= min and n <= max
        return False
    

    
    def input(self, question: str, default='', canBeBlank=True):
        answer = None
        while answer == None or (answer == '' and not canBeBlank):
            answer = input(question)
        
        return default if answer == '' else answer
    

    def getAlphaNumeric(self, question: str, max: int, choices: list, min = 1, caseSensitive = False):
        choice = ''
        
        while not (self._isNumberInRange(choice, max, min) or self._isLetterInChoices(choice, choices, caseSensitive)):
            choice = self.input(question)

        # Return as an int if a number was chosen
        if choice.isdigit():
            return int(choice)
        
        # Return letters (lowercased if required)
        return choice if caseSensitive else choice.lower()
    

    def getNumber(self, question: str, max: int, min = 1, canQuit = False) -> int:
        choice = ''
        first = True

        while not self._isNumberInRange(choice, max, min):

            if (not first):
                print("Invalid Entry")
            first = False
            choice = self.input(question)
            if canQuit and self._isLetterInChoices(choice, ['q']):
                return 'q'
        
        return int(choice)
    

    def getLetter(self, question: str, choices: list, caseSensitive = False, default = None) -> str:
        choice = ''
        
        if default == None:
            # If there's no default option, keep asking the question until given a proper input
            while not self._isLetterInChoices(choice, choices, caseSensitive):
                choice = self.input(question)
        else:
            # If there's a default option, then invalid responses should be the default
            choice = self.input(question)
            if not self._isLetterInChoices(choice, choices, caseSensitive):
                choice = default
        
        return choice if caseSensitive else choice.lower()
    

    def getOrg(self, question: str, default = '', levels = [6]) -> str:
        # Levels:
        # level 4: region
        # level 5: NRA
        # level 6: truic
        choice = ''
        
        while not any([self._isOrgValid(choice, l) for l in levels]):
            choice = self.input(question)
            if choice == '':
                choice = default
        
        if len(levels) == 1:
            return choice
        
        # If there's a range of what level could have been selected,
        # inform the caller about which level the input org is.
        for level in levels:
            if self._isOrgValid(choice, level):
                return choice, level
    

    def menu(self) -> None:
        input('Menu for tool has not been defined! Press Enter to continue.')
    

    def enterSubmenu(self, submenu: Callable, *args):
        try:
            submenu(*args)
        except KeyboardInterrupt:
            print(utils.COLORCANCEL + '\n\nCancelled. Returning...\n' + utils.COLORRESET)
            utils.wait(0.7)
