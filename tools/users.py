import utils
from .testingTool import TestingTool
import string

class UserTool(TestingTool):
    iUsedToBeId = None
    iWantToBeId = None

    def menu(self) -> None:
        displayColumns = ['id', 'dodId', 'firstName', 'lastName', 'uic', 'email', 'accountStatus', 'archive']
        query = 'select * from [Base].[User]'
        
        myDodId = self.config['User']['DodId']

        def colorRuleSwappingUsers(row: dict):
            if 'dodId' in row and row['dodId'] == myDodId:
                return utils.COLORCURRENTUSER
            if 'dodId' in row and row['dodId'] == self.iUsedToBeId:
                return utils.COLOROLDUSER
            if 'dodId' in row and row['dodId'] == '0000000000':
                return utils.COLORSYSTEMUSER
            return utils.COLORRESET

        choice = None
        while choice != 'q':
            print(f"{'='*10} User Management {'='*10}")
            print('(green = you right now, cyan = who you last swapped to)')
            print()

            users = self.db.fetchRows(query)
            users = users[1:] # remove System user
            utils.printRows(users, displayColumns, colorRuleSwappingUsers)
            print()

            print('Actions: (r)eset your login, change (u)nit, (s)et account status, (a)rchive a user, (+) add a user, (q)uit')
            choice = self.getAlphaNumeric('Which user would you like to become? > ', len(users), ['r', 'u', 's', 'a', '+', 'q'])
            if isinstance(choice, int):
                self.iWantToBeId = users[choice - 1]['dodId']
                self.iUsedToBeId = self._swapUsers(myDodId)
                self._resetLogin(myDodId)
            else:
                if choice == 'r':
                    self._resetLogin(myDodId)
                elif choice == 'u':
                    self.enterSubmenu(self._changeUnit, users)
                elif choice == 's':
                    self.enterSubmenu(self._setUserStatus, users)
                elif choice == 'a':
                    self.enterSubmenu(self._archiveUser, users)
                elif choice == '+':
                    self.enterSubmenu(self._addUser, users)
            
            utils.clearScreen()

    
    def _swapUsers(self, myId):
        undoSwap = self.iWantToBeId == self.iUsedToBeId
        queries = []

        if self.iUsedToBeId is not None and not undoSwap:
            # Mark our old, real user row with a placeholder
            queries.append(f"update [Base].[User] set [dodId]='tester' where [dodId]='{self.iUsedToBeId}'")

            # Put the other user's ID back where it belongs
            queries.append(f"update [Base].[User] set [dodId]='{self.iUsedToBeId}' where [dodId]='{myId}'")
        else:
            # Mark our current user row with a placeholder
            queries.append(f"update [Base].[User] set [dodId]='tester' where [dodId]='{myId}'")

        # Swap our ID onto the user we want
        queries.append(f"update [Base].[User] set [dodId]='{myId}' where [dodId]='{self.iWantToBeId}'")

        # Store the other user's ID in the placeholder
        queries.append(f"update [Base].[User] set [dodId]='{self.iWantToBeId}' where [dodId]='tester'")

        # Complete transaction
        self.db.executeAll(queries)
        return self.iWantToBeId if not undoSwap else None


    def _resetLogin(self, dodId):
        userIds = self.db.fetchRows(f"select top 1 [id] from [Base].[User] where [dodId]='{dodId}'")
        userId = userIds[0]['id']
        self.db.execute(f"delete from [Base].[UserLogin] where [userId]={userId}")


    def _setUserStatus(self, users: list):
        choice = self.getNumber('Which user to set account status? > ', len(users))

        print(' 1 = active')
        print(' 0 = inactive due to inactivity')
        print('-1 = disabled due to inactivity')
        status = self.getNumber('Set account status to? > ', 1, -1)

        self.db.execute(f"update [Base].[User] set [accountStatus]={status} where [dodId]='{users[choice - 1]['dodId']}'")


    def _archiveUser(self, users: list):
        choice = self.getNumber('Which user to toggle archival? > ', len(users))
        self.db.execute(f"update [Base].[User] set [archive]='{not users[choice - 1]['archive']}' where [dodId]='{users[choice - 1]['dodId']}'")
    

    def _addUser(self, users):
        choice = self.getLetter('\nDo you want to (s)pecify the user\'s values, use (r)andomized values, or create your (d)efault user? > ', ['s', 'r', 'd'])
        if choice == 'd':
            self._addUserDefault()
        elif choice == 's':
            self._addUserManually(users)
        elif choice == 'r':
            self._addUserRandomly(users)
    
    
    def _addUserDefault(self):
        existingUsers = self.db.fetchRows(f"select top 1 * from [Base].[User] where [dodId] = '{self.config['User']['DodId']}'")
        if len(existingUsers) > 0:
            print(f"\nDefault user already exists (user {existingUsers[0]['id']})!\nNo user has been created.")
            input('(Press Enter to continue.) ')
            return
        
        dodId = self.config['User']['DodId']
        firstName = self.config['User']['FirstName']
        lastName = self.config['User']['LastName']
        email = self.config['User']['Email']
        unit = self.config['User']['Unit']
        
        altEmail = email
        middleName = 'Z'
        phone = '7575555555'
        ims = 'RD2'
        mas = 'PRO'
        pay = 1
        current = 1
        rtng_desg = ''
        rate_rank = ''

        self.db.execute(f"insert into [Base].[QPers] ([dodId], [firstName], [middleName], [lastName], [unit], [email], [altEmail], [phone], [ims], [mas], [pay], [current], [rtng_desg], [rate_rank]) values ('{dodId}', '{firstName}', '{middleName}', '{lastName}', '{unit}', '{email}', '{altEmail}', '{phone}', '{ims}', '{mas}', '{pay}', '{current}', '{rtng_desg}', '{rate_rank}')")
        self.db.execute(f"insert into [Base].[User] ([dodId], [firstName], [middleName], [lastName], [uic], [email], [altEmail], [phone], [department], [designation], [accountStatus], [archive], [createdById], [createdDate]) values ('{dodId}', '{firstName}', '{middleName}', '{lastName}', '{unit}', '{email}', '{altEmail}', '{phone}', 'N36', 'CTR', 1, 0, 1, GETDATE())")
    
    
    def _addUserManually(self, users: list):
        dodId = ''
        takenIds = [u['dodId'] for u in users]
        while dodId == '':
            dodId = self.input(f"DoD ID? > ", canBeBlank=False)
            if dodId in takenIds:
                print('\nThat DoD ID is already in use.')
                dodId = ''

        print('\nThe following options default to your settings. Press Enter to use the default, or type your desired value.')
        firstName = utils.escapeDbString(self.input(f"First name? {utils.COLORDEFAULTINPUT}[default: {self.config['User']['FirstName']}]{utils.COLORRESET} > ", self.config['User']['FirstName']))
        lastName = utils.escapeDbString(self.input(f"Last name? {utils.COLORDEFAULTINPUT}[default: {self.config['User']['LastName']}]{utils.COLORRESET} > ", self.config['User']['LastName']))
        email = self.input(f"Email? {utils.COLORDEFAULTINPUT}[default: {self.config['User']['Email']}]{utils.COLORRESET} > ", self.config['User']['Email'])
        unit = self.getOrg(f"Unit UIC? {utils.COLORDEFAULTINPUT}[default: {self.config['User']['Unit']}]{utils.COLORRESET} > ", self.config['User']['Unit'], levels=[6])
        
        print('\nThe remaining options provide a reasonable default. Press Enter to use the default, or type your desired value.')
        altEmail = self.input(f"Alt email? {utils.COLORDEFAULTINPUT}[default: {email}]{utils.COLORRESET} > ", email)
        middleName = utils.escapeDbString(self.input(f"Middle name? {utils.COLORDEFAULTINPUT}[default: Z]{utils.COLORRESET} > ", 'Z'))
        phone = self.input(f"Phone? {utils.COLORDEFAULTINPUT}[default: 7575555555]{utils.COLORRESET} > ", '7575555555')
        ims = self.input(f"IMS? {utils.COLORDEFAULTINPUT}[default: RD2]{utils.COLORRESET} > ", 'RD2')
        mas = self.input(f"MAS? {utils.COLORDEFAULTINPUT}[default: PRO]{utils.COLORRESET} > ", 'PRO')
        pay = self.input(f"Pay? {utils.COLORDEFAULTINPUT}[default: 1]{utils.COLORRESET} > ", 1)
        current = self.input(f"Current? {utils.COLORDEFAULTINPUT}[default: 1]{utils.COLORRESET} > ", 1)
        rtng_desg = ''
        rate_rank = ''

        self.db.execute(f"insert into [Base].[QPers] ([dodId], [firstName], [middleName], [lastName], [unit], [email], [altEmail], [phone], [ims], [mas], [pay], [current], [rtng_desg], [rate_rank]) values ('{dodId}', '{firstName}', '{middleName}', '{lastName}', '{unit}', '{email}', '{altEmail}', '{phone}', '{ims}', '{mas}', '{pay}', '{current}', '{rtng_desg}', '{rate_rank}')")
        self.db.execute(f"insert into [Base].[User] ([dodId], [firstName], [middleName], [lastName], [uic], [email], [altEmail], [phone], [department], [designation], [accountStatus], [archive], [createdById], [createdDate]) values ('{dodId}', '{firstName}', '{middleName}', '{lastName}', '{unit}', '{email}', '{altEmail}', '{phone}', 'N36', 'CTR', 1, 0, 1, GETDATE())")
    
    
    def _addUserRandomly(self, users):
        numNewUsers = self.getNumber('How many new users would you like generate? (up to 9999) > ', 9999)

        minDodId = 100
        maxDodId = 99999
        lengthDodId = 5
        padDodId = '0'
        takenIds = [u['dodId'] for u in users]
        firstNames = ['Test', 'Tester', 'Mr', 'Ms', 'Mrs', 'Dr', 'FirstName', 'Random', 'Cathy', 'Justin', 'Kenny', 'Jacob', 'Daniel', 'Brittanie', 'Shirley']
        lastNames = ['Test', 'Tester', 'McTester', 'Jr', 'LastName', 'McLastName', 'Random', 'Person']

        for _ in range(numNewUsers):
            dodId = ''
            while dodId == '' or dodId in takenIds:
                dodId = str(utils.randomInt(minDodId, maxDodId)).rjust(lengthDodId, padDodId)
            takenIds.append(dodId)

            firstName = utils.randomChoice(firstNames)
            lastName = utils.randomChoice(lastNames)
            email = self.config['User']['Email']
            unit = self.config['User']['Unit']
            
            altEmail = email
            middleName = utils.randomChoice(string.ascii_uppercase)
            phone = '757' + str(utils.randomInt(1111111, 9999999))
            ims = 'RD2'
            mas = 'PRO'
            pay = 1
            current = 1
            rtng_desg = ''
            rate_rank = ''

            self.db.execute(f"insert into [Base].[QPers] ([dodId], [firstName], [middleName], [lastName], [unit], [email], [altEmail], [phone], [ims], [mas], [pay], [current], [rtng_desg], [rate_rank]) values ('{dodId}', '{firstName}', '{middleName}', '{lastName}', '{unit}', '{email}', '{altEmail}', '{phone}', '{ims}', '{mas}', '{pay}', '{current}', '{rtng_desg}', '{rate_rank}')")
            self.db.execute(f"insert into [Base].[User] ([dodId], [firstName], [middleName], [lastName], [uic], [email], [altEmail], [phone], [department], [designation], [accountStatus], [archive], [createdById], [createdDate]) values ('{dodId}', '{firstName}', '{middleName}', '{lastName}', '{unit}', '{email}', '{altEmail}', '{phone}', 'N36', 'CTR', 1, 0, 1, GETDATE())")


    def _changeUnit(self, users):
        choice = self.getNumber('Which user to change unit? > ', len(users))
        dodId = users[choice - 1]['dodId']
        newUnit = self.getOrg('Which unit to change to? > ', levels=[6])

        self.db.execute(f"update [Base].[QPers] set [unit]='{newUnit}' where [dodId]='{dodId}'")
        self.db.execute(f"update [Base].[User] set [uic]='{newUnit}' where [dodId]='{dodId}'")
