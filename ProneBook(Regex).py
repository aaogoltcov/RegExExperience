import re
import csv

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Разделение ФИО
contacts_list_new = list()
for person in contacts_list[1:len(contacts_list)]:
    contacts_list_person = list()
    for item in person[0:2]:
        contacts_list_person.extend(re.findall(r"\w+", item))
    while len(contacts_list_person) < 3:
        contacts_list_person.append("")
    contacts_list_new.append(contacts_list_person)

# Подготовка словаря для контакта
person_info_list = {}
for item in contacts_list[0]:
    person_info_list.update({item: ''})
contacts_list.remove(contacts_list[0])

# Получение нового списка с разделенным ФИО
contacts_list_treated = list()
for i, person in enumerate(contacts_list):
    contacts_list_person = list()
    contacts_list_person.extend(contacts_list_new[i])
    contacts_list_person.extend(person[3:len(person)])
    contacts_list_treated.append(contacts_list_person)

# Приведение записной книжки к словарю
phonebook_list = list()
for person in contacts_list_treated:
    person_info_dict = dict()
    for i, key in enumerate(person_info_list.keys()):
        person_info_item = {key: person[i]}
        person_info_dict.update(person_info_item)
    phonebook_list.append(person_info_dict)

# Объединение одинаковых контактов
phonebook_list_new = list()
for item in phonebook_list:
    for another_item in phonebook_list:
        new_item = item
        if (item['lastname'] == another_item['lastname']) \
                and (item['firstname'] == another_item['firstname']) \
                and (item != another_item):
            new_item = dict()
            for key, value in item.items():
                if value:
                    new_item.update({key: value})
                else:
                    new_item.update({key: another_item[key]})
            break
    phonebook_list_new.append(new_item)
phonebook_list_clear = list()
for item in phonebook_list_new:
    if not item in phonebook_list_clear:
        phonebook_list_clear.append(item)

# Приведение номеров телефонов к заданому формату
for person in phonebook_list_clear:
    person['phone'] = re.compile(r"((8(\s|\()?)|(\+7\s?\(?))(\d{0,3})(\)?"
                                 r"\s?-?)(\d+)(\-?)(\d+)(-?)(\d+)((\s)\(?"
                                 r"(доб.)\s)?(\d+)?\)?").sub(r"+7(\5)\7\9"
                                 r"\11\13\14\15", person['phone'])

# Запись файла в формате CSV
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(phonebook_list_clear[0].keys())
    for person in phonebook_list_clear:
        datawriter.writerow(person.values())
    print('Done!')
