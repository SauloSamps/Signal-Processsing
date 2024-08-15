import os
from Content.Interface.interface_control import Interface

def main():
    interface = Interface()
    intro_message = open("Content/Interface/Messages/intro.txt", 'r')
    print(intro_message.read())
    while(True):
        user_input = input(">>>")
        quit_status = interface.receive_command(user_input)

        if(quit_status):
            print("Exiting the program...")
            break

if __name__ == '__main__':
    main()
