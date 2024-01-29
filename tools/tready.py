import utils
from .testingTool import TestingTool

class TReadyTool(TestingTool):
    def menu(self) -> None:
        print(f"{'='*10} Editing T-Ready Requirements {'='*10}")
        print()

        # Get DoD ID
        dodId = self.input(f"DoD ID of user to edit? > ", canBeBlank=False)
        print()

        # Get BIN
        bin = self.input(f"BIN of user to edit? > ", canBeBlank=False)
        print()

        self.enterSubmenu(self._manageUser, dodId, bin)
        
        utils.clearScreen()


    def _manageUser(self, dodId, bin):
        displayColumns = ['dispName', 'status']
        query = f"select * from [TReady].[vRequirementCompletionUMUIC] [r] inner join [TReady].[Category] [c] on [r].[category] = [c].[id] where [dodId]='{dodId}' and [BIN]='{bin}'"

        user = self.db.fetchRows(f"select top(1) * from [Base].[QPers] where [dodId]='{dodId}'")
        if len(user) == 0:
            print(f"The DoD ID you entered ({dodId}) does not belong to a user.\nPress Enter to continue.")
            input()
            return
        user = user[0]

        choice = None
        while choice != 'q':
            utils.clearScreen()

            requirements = self.db.fetchRows(query)
            print(f"{'='*10} {user['firstName']} {user['lastName']}, BIN {bin}: {'='*10}")
            utils.printRows(requirements, displayColumns, numberRows=True)
            print()

            print('Actions: (q)uit')
            choice = self.getNumber('Which requirement to update? > ', len(requirements), canQuit=True)
            if choice != 'q':
                self.enterSubmenu(self._updateRequirement, requirements[choice - 1])
    

    def _updateRequirement(self, requirement):
        choice = self.getLetter('Set requirement to which status? [C, I, NA] > ', ['C', 'I', 'NA']).lower()
        choice = choice.upper()
        
        existingRow = self.db.fetchRows(f"select top(1) * from [TReady].[Completion] where [reqId]={requirement['reqId']} and [dodId]={requirement['dodId']}")

        if len(existingRow) == 0:
            self.db.execute(f"insert into [TReady].[Completion] values ({requirement['reqId']}, '{requirement['dodId']}', getdate(), '{choice}', getdate(), getdate(), {requirement['category']})")
        else:
            existingRow = existingRow[0]
            self.db.execute(f"update [TReady].[Completion] set [status]='{choice}' where [id]={existingRow['id']}")
