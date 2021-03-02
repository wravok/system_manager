def load_systems_list(collection):
    systems = []
    for item in collection.systems.find({}, {'_id': 1, 'system': 1}):
        systems.append(item)

    return systems


def remove_system_item(sys_id, item, collection):
    system = {'_id': sys_id}
    item = {'$unset': {item: ""}}
    result = collection.systems.update(system, item)
    return result


def remove_system(sys_id, collection):
    system = {'_id': sys_id}
    result = collection.systems.remove(system)
    return result


def add_system(item, collection):
    result = collection.systems.insert_one(item)
    return result


def get_system_properties(sys_id, collection):
    prop_list = []
    item = collection.systems.find_one({'_id': sys_id}, {'_id': 0})

    for k, v in item.items():
        prop_list.append([k, v])

    return prop_list


def print_system_details(details):
    system_details = ''
    system_header = 'Details for unknown system:\n\n'

    for i, item in enumerate(details):
        if item[0] != 'system':
            system_details += (f'  {i:2d} - {item[0]}: {item[1]}\n')
        else:
            system_header = (f'Details for system: {item[1]}\n\n')

    return system_header + system_details


def update_system_item(id, item, new_value, collection):

    new_val = {item: new_value}
    result = collection.systems.update_one(
        {"_id": id},
        {"$set": new_val},
        upsert=True
    )

    return result


if __name__ == '__main__':
    pass
