import utils
from .testingTool import TestingTool

class EmailTool(TestingTool):
    def menu(self) -> None:
        systemEmails = [
            self.config['Emails']['Bridge'],
            self.config['Emails']['ARQ'],
            self.config['Emails']['TReady'],
        ]

        print(f"{'='*10} Queueing a Test Email {'='*10}")
        print()

        # Get subject
        subject = utils.escapeDbString(self.input('Subject: ', canBeBlank=False))
        print()

        # Get body
        body = utils.escapeDbString(self.input('Body: ', canBeBlank=False))
        print()

        # Get to address
        to = self.getLetter(f"To (y)ou at {self.config['User']['Email']}, a (u)ser, or an (e)mail address? > ", ['y', 'u', 'e'])
        if to == 'y':
            to = self.config['User']['Email']
        elif to == 'u':
            users = self.db.fetchRows('select * from [Base].[User]')
            users = users[1:] # remove System user
            print()
            utils.printRows(users, ['dodId', 'firstName', 'lastName', 'email'])
            print()
            
            toUser = self.getNumber('To which user? > ', len(users))
            to = users[toUser - 1]['email']
        elif to == 'e':
            to = self.input('Enter an email address: ', canBeBlank=False)
        print()

        # Get from address
        i = 1
        for e in systemEmails:
            print(f"{i}. {e}")
            i += 1
        from_ = self.getNumber('From which system? > ', len(systemEmails))
        from_ = systemEmails[from_ - 1]
        print()
        
        # Send the email
        try:
            body = body.replace("'", "\'")
            subject = subject.replace("'", "\'")
            to = to.replace("'", "\'")
            from_ = from_.replace("'", "\'")
            self.db.execute(f"insert into [Base].[Email] ([body], [subject], [to], [from]) values ('{body}', '{subject}', '{to}', '{from_}')")
            input('Email queued, enter to continue. ')
        except:
            input('Error attempting to queue email! Enter to continue. ')
