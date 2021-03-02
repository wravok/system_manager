from utils.utils import clear, connect_mongo_db, get_sys_db_params
from systemmanager import systemanager
import json
from time import sleep


def print_systems():
    print('Please select a system: ')

    for i in range(len(systems)):
        try:
            print(f'  {i:2d} - {systems[i]["system"]}')
        except KeyError:
            print(f'  {i:2d} - *** Unkown ***')


def select_system():
    clear()
    print_systems()
    print(f'\n New - Add new system')
    print(f' Del - Delete a system')
    print(f'Exit - Exit program')
    return input('\nPlease select an option: ')


def update_system_item(id, item):
    clear()
    print(f'Changing value for {item[0]}.\nCurrent value: {item[1]}\n')
    new_value = input(f'Enter new value:')
    systemanager.update_system_item(id, item[0], new_value, mdb)


def delete_system_item(sys_id):
    details = systemanager.get_system_properties(sys_id, mdb)
    clear()
    print(systemanager.print_system_details(details))
    print(f'Exit - to abort DELETE')

    del_item = input(f'Select item to be DELETED: ')
    if del_item.isdigit() and int(del_item) < (len(details)):
        systemanager.remove_system_item(sys_id, details[int(del_item)][0], mdb)
    elif del_item.lower() == 'exit':
        pass
    else:
        print(f'not a valid option. Aborting delete')
        sleep(2)
    return True


def new_system_item(sys_id):
    clear()
    item = input(f'enter new item name: ')
    value = input(f'enter item value: ')
    systemanager.update_system_item(sys_id, item, value, mdb)


def system_menu(id):
    while True:
        details = systemanager.get_system_properties(id, mdb)

        clear()
        print(systemanager.print_system_details(details))
        print(f' New - Add new item')
        print(f' Del - Delete an item')
        print(f'Exit - Return to main menu')
        action = input(
            '\nSelect item an option: ')

        if action.isdigit() and int(action) < (len(details)):
            result = update_system_item(id, details[int(action)])
        elif action.lower() == 'exit':
            break
        elif action.lower() == 'new':
            result = new_system_item(id)
        elif action.lower() == 'del':
            delete_system_item(id)

        else:
            print('Please enter a valid option!\n')
            sleep(2)

    return None


def new_system():
    clear()
    system = input('Please enter the system name:')
    systemanager.add_system({'system': system}, mdb)


def del_system():
    systems = systemanager.load_systems_list(mdb)
    clear()
    print_systems()
    print(f'\nExit - Exit program')
    sys_del = input('\nPlease select system to DELETE: ')
    if sys_del.isdigit() and int(sys_del) < (len(systems)):
        systemanager.remove_system(systems[int(sys_del)]["_id"], mdb)
    elif sys_del.lower() == 'exit':
        pass
    else:
        print(f'not a valid option. Aborting delete')
        sleep(2)
    return True


params = get_sys_db_params('config.ini')

# dbpass = input("Enter master password:")
mdb = connect_mongo_db(params['user'], params['pwd'], params['host'])

while True:
    clear()
    systems = systemanager.load_systems_list(mdb)
    option = select_system()
    if option.isdigit() and int(option) < len(systems):
        system_menu(systems[int(option)]["_id"])
    elif option.lower() == 'exit':
        break
    elif option.lower() == 'new':
        new_system()
    elif option.lower() == 'del':
        del_system()
        continue
    else:
        print('Please enter a valid option!\n')
        sleep(2)
