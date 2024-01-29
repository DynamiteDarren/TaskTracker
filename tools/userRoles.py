import utils
from .testingTool import TestingTool

class UserRoleTool(TestingTool):
    def menu(self) -> None:
        displayColumns = ['id', 'dodId', 'firstName', 'lastName', 'uic']
        query = 'select * from [Base].[User]'
        
        myDodId = self.config['User']['DodId']

        def colorRuleUsers(row: dict):
            if 'dodId' in row and row['dodId'] == myDodId:
                return utils.COLORCURRENTUSER
            if 'dodId' in row and row['dodId'] == '0000000000':
                return utils.COLORSYSTEMUSER
            return utils.COLORRESET

        choice = None
        while choice != 'q':
            print(f"{'='*10} User Role Management {'='*10}")
            print('(green = you right now)')
            print()

            users = self.db.fetchRows(query)
            users = users[1:] # remove System user
            utils.printRows(users, displayColumns, colorRuleUsers)
            print()

            print('Actions: (q)uit')
            choice = self.getNumber('Which user would you like to manage? > ', len(users), canQuit=True)
            if isinstance(choice, int):
                user = users[choice - 1]
                self.enterSubmenu(self._manageUser, user)
            
            utils.clearScreen()


    def _manageUser(self, user: dict):
        userId = user['id']

        displayColumns = ['id', 'roleName', 'data', 'status']
        query = f"select * from [Base].[UserRole] where [userId]={userId}"

        choice = None
        while choice != 'q':
            utils.clearScreen()

            print(f"{'='*10} {user['firstName']} {user['lastName']}'s current roles: {'='*10}")
            roles = self.db.fetchRows(query)
            utils.printRows(roles, displayColumns)
            print()

            print('Actions: (a)dd, (u)pdate, (d)elete, change (s)tatus, (q)uit')
            choice = self.getLetter('Which action would you like to take? > ', ['a', 'u', 'd', 's', 'q'])
            if choice == 'a':
                self.enterSubmenu(self._addUserRole, userId)
            elif choice == 'u':
                self.enterSubmenu(self._updateUserRole, roles)
            elif choice == 'd':
                self.enterSubmenu(self._deleteUserRole, userId, roles)
            elif choice == 's':
                self.enterSubmenu(self._setRoleStatus, roles)
    

    def _addUserRole(self, userId):
        systems = ['Bridge', 'ARQ', 'T-Ready']
        print()
        for i in range(len(systems)):
            print(f"{i + 1}. {systems[i]}")
        
        system = self.getNumber('Which system is the role for? > ', len(systems))
        system = systems[system - 1]

        roleName, data = self._createUserRoleAndData(system)
        
        self.db.execute(f"insert into [Base].[UserRole] ([userId], [roleName], [data], [status], [createdById], [createdDate]) values ({userId}, '{roleName}', {data}, 1, 1, GETDATE())")
    

    def _updateUserRole(self, roles):
        role = self.getNumber('Which role would you like to update? > ', len(roles))
        role = roles[role - 1]

        system = role['roleName'].split(':')[0]
        roleId = role['id']
        roleName, data = self._createUserRoleAndData(system)

        self.db.execute(f"update [Base].[UserRole] set [roleName]='{roleName}', [data]={data} where [id]={roleId}")
    

    def _deleteUserRole(self, userId, roles: list):
        role = self.getNumber('Which role would you like to delete? > ', len(roles))
        role = roles[role - 1]
        self.db.execute(f"delete from [Base].[UserRole] where [userId]={userId} and [roleName]='{role['roleName']}'")
    

    def _setRoleStatus(self, roles):
        role = self.getNumber('Which role would you like to set status for? > ', len(roles))
        role = roles[role - 1]
        roleId = role['id']

        print(' 1 = active')
        print(' 0 = inactive')
        print('-1 = disabled')
        status = self.getNumber('Set account status to? > ', 1, -1)

        self.db.execute(f"update [Base].[UserRole] set [status]={status} where [id]={roleId}")


    def _createUserRoleAndData(self, system) -> tuple:
        role = ''
        roles = [utils.removeprefix(r, f"{system}:") for r in utils.roleToLevel.keys() if r.find(f"{system}:") == 0]
        
        print()
        for i in range(len(roles)):
            print(f"{i + 1}. {roles[i]}")
        
        role = self.getNumber('Which role would you like? > ', len(roles))
        role = roles[role - 1]

        roleName = f"{system}:{role}"
        level = utils.roleToLevel[roleName]

        if level > 2:
            ids = self.input('Enter UICs, separated by commas: > ')
            ids = [id.strip() for id in ids.split(',') if self._isOrgValid(id.strip(), level)]
            data = f"'{utils.createRoleData(ids, level)}'"
        else:
            data = 'null'
        
        return (roleName, data)
