import os
from Content.Scripts.controller import Controller

class Interface:
    def __init__(self):
        self.controller = Controller()
        self.messages_path = "Content/Interface/Messages/"
        self.available_commands = ["quit", "clear"]

        return None
    
    def help(self, command=False):
        
        if command:
            if command in self.available_commands:
                reply = open(self.messages_path + str(command)+".txt", 'r')
                print(reply.read() + "\n\n")
            else:
                print("No such command\n\n")
        else:
            reply  = open(self.messages_path + "help_generic.txt", 'r')
            print(reply.read() + "\n\n")

            

    def receive_command(self, command):
        command = command.split()

        match(command[0]):

            case 'help':
                command_specified = False
                if (len(command) > 1):
                    command_specified = command[1]
                self.help(command_specified)
            case 'clear':
                os.system('cls')
            case 'quit':
                return True
            case 'generate-data':
                pass


        