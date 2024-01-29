
import json
import sys
import time
import random


def wait(seconds: float):
    time.sleep(seconds)


def exit():
    sys.exit()


def exitWithError(e: Exception, messageSubject: str, messageDescription = ''):
    print(e)
    print(f"\n=== {messageSubject} ===")


    if messageDescription != '':
        print(messageDescription)
        print()
    
    print('(Your database has been left unharmed.)\n')
    exit()


def clearScreen():
    # https://stackoverflow.com/a/50560686
    print('\033c', end='')


def filterRows(rows: list, desiredFields: list) -> list:
    filteredRows = []
    for r in rows:
        filteredRows.append({k: r[k] for k in r.keys() if k in desiredFields})
    return filteredRows


def getRowWidths(rows: list, desiredFields = None) -> list:
    widths = []

    # Include headers
    headers = desiredFields if desiredFields != None else list(rows[0].keys())

    for i in range(len(headers)):
        # Start by assuming that the column header is longest
        longest = len(str(headers[i]))

        # Check each row value for a longer one
        for r in rows:
            value = r[headers[i]]
            length = len(str(value))
            if length > longest:
                longest = length
        
        widths.append(longest)
    return widths


def printRows(rows: list, desiredFields = None, colorRules = None, numberRows = True):
    spacer = '  '
    rowNumber = 1

    if len(rows) == 0:
        return

    # Find longest column for nice table printing
    widths = getRowWidths(rows, desiredFields)

    # Print headers
    headers = desiredFields if desiredFields != None else list(rows[0].keys())
    if numberRows:
        print('#'.ljust(3 + len(spacer), ' '), end='')
    for i in range(len(headers)):
        h = str(headers[i])
        print(h.ljust(widths[i], ' '), end='')
        print(spacer, end='')
    print()

    # Print rows
    for r in rows:
        # Set up colored text, if applicable
        if colorRules:
            print(colorRules(r), end='')
        
        if numberRows:
            print(f"{rowNumber}.".ljust(3, ' '), end='')
            print(spacer, end='')

        for i in range(len(headers)):
            value = r[headers[i]]
            print(str(value).ljust(widths[i], ' '), end='')
            print(spacer, end='')

        # Prep for next row
        rowNumber += 1


def randomizeSeed():
    random.seed()

def randomInt(minInclusive: int, maxInclusive: int) -> int:
    return random.randint(minInclusive, maxInclusive)

def randomChoice(sequence):
    return random.choice(sequence)


def escapeDbString(s: str) -> str:
    # SQL requires single quotes to be escaped
    return s.replace("'", "''")


def removeprefix(s: str, prefix: str) -> str:
    if s.startswith(prefix):
        s = s[len(prefix):]
    return s


def removesuffix(s: str, suffix: str) -> str:
    if s.endswith(suffix):
        s = s[:-len(suffix)]
    return s


