import utils
from .testingTool import TestingTool

class UnitLookupTool(TestingTool):
    recentHierarchies = []
    maxRecent = 5

    def menu(self) -> None:
        choice = None
        while choice != 'q':
            print(f"{'='*10} Unit Lookup {'='*10}")
            print()

            if len(self.recentHierarchies) > 0:
                print(f"Your {len(self.recentHierarchies)} most recently viewed hierarchies:")
                self.recentHierarchies.reverse()
                utils.printRows(self.recentHierarchies, ['regionTitle', 'region', 'nraTitle', 'nra', 'ruicTitle', 'ruic'], numberRows=False)
                self.recentHierarchies.reverse()
                print()

            print('Actions: (l)ookup an org\'s hierarchy, (s)earch for a unit, find (r)andom unit, see (m)embers in a unit, (q)uit')
            choice = self.getLetter('What would you like to do? > ', ['l', 's', 'r', 'm', 'q'])
            if choice == 'l':
                self.enterSubmenu(self._lookupOrg)
            elif choice == 's':
                self.enterSubmenu(self._searchForUnit)
            elif choice == 'r':
                self.enterSubmenu(self._findRandomUnit)
            elif choice == 'm':
                self.enterSubmenu(self._seeMembersInUnit)
            
            utils.clearScreen()
    

    def _addToRecentHierarchies(self, hierarchy):
        self.recentHierarchies.append(hierarchy)
        if len(self.recentHierarchies) > self.maxRecent:
            startFrom = len(self.recentHierarchies) - self.maxRecent
            self.recentHierarchies = self.recentHierarchies[startFrom:]
    

    def _lookupOrg(self):
        print()
        org, level = self.getOrg('See the hierarchy of which org? > ', levels=[6, 5, 4])
        hierarchy = self._getHierarchy(org, level=level)
        self._addToRecentHierarchies(hierarchy)

        if level == 6:
            print('\nThat unit\'s hierarchy is:')
        else:
            print(f"\nA random unit in that {utils.levelToOrg[level]} is:")
        self._printHierarchy(hierarchy)
        input('\nPress Enter to continue.')
    

    def _searchForUnit(self):
        print()
        minMembers = self.getNumber('Unit should have at least how many members? > ', 99999, 0)
        maxMembers = self.getNumber('Unit should have at most how many members? > ', 99999, minMembers)

        unit = self.db.fetchRows(f"select top(1) [unit] from [Base].[QPers] group by [unit] having count([unit]) >= {minMembers} and count([unit]) <= {maxMembers} order by newid()")
        if len(unit) == 0:
            input('\nThere are no units matching your query.\nPress Enter to continue.')
            return
        unit = unit[0]['unit']
        hierarchy = self._getHierarchy(unit)
        self._addToRecentHierarchies(hierarchy)

        print('\nA random unit matching your query is:')
        self._printHierarchy(hierarchy)
        input('\nPress Enter to continue.')
    

    def _findRandomUnit(self):
        unit = self.db.fetchRows(f"select top(1) [unit] from [Base].[QPers] order by newid()")
        unit = unit[0]['unit']
        hierarchy = self._getHierarchy(unit)
        self._addToRecentHierarchies(hierarchy)

        print('\nA random unit is:')
        self._printHierarchy(hierarchy)
        input('\nPress Enter to continue.')
    

    def _seeMembersInUnit(self):
        displayColumns = ['dodId', 'firstName', 'lastName', 'unit', 'email']

        print()
        unit = self.getOrg('View members of which unit? > ', levels=[6])
        members = self.db.fetchRows(f"select * from [Base].[QPers] where [unit] = '{unit}'")

        utils.printRows(members, displayColumns)
        
        input('\nPress Enter to continue.')
    

    def _printHierarchy(self, hierarchy):
        longest = max([len(t) for t in [hierarchy[title] for title in ['hqTitle', 'commandTitle', 'regionTitle', 'nraTitle', 'ruicTitle']]])
        print(f"     HQ: {hierarchy['hqTitle'].rjust(longest, ' ')} ({hierarchy['hqUic']})")
        print(f"Command: {hierarchy['commandTitle'].rjust(longest, ' ')} ({hierarchy['commandUic']})")
        print(f" Region: {hierarchy['regionTitle'].rjust(longest, ' ')} ({hierarchy['region']})")
        print(f"    NRA: {hierarchy['nraTitle'].rjust(longest, ' ')} ({hierarchy['nra']})")
        print(f"   Unit: {hierarchy['ruicTitle'].rjust(longest, ' ')} ({hierarchy['ruic']})")
    

    def _getHierarchy(self, org, level=6):
        hierarchy = self.db.fetchRows(f"select top(1) [hqUic], [hqTitle], [commandUic], [commandTitle], [region], [regionTitle], [nra], [nraTitle], [ruic], [ruicTitle] from [Base].[Hierarchy] where [{utils.levelToOrg[level]}]='{org}' order by newid()")
        return hierarchy[0]
