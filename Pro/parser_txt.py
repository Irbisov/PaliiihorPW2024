from Adress_book import Record, AddressBook
import re


def read_txt():
    dict = {}
    ls = []
    path = "users_inform.txt"
    with (open(path, 'r') as fh):
        line = fh.readlines()
        if len(line) == 0:
            pass
        else:
            for i in line:
                parse_line = parse_log_line(i)
                dict[parse_log_line(i).get('name')] = parse_line
                sample = Record(parse_line.get('name'))
                for i in parse_line.get('phones'):
                    sample.add_phone(i)
                sample.add_birthday(parse_line.get('birthday'))
                ls.append(sample)
        return ls


def parse_log_line(i: str) -> dict:
    match_dict = {}
    ls = []
    pattern = r"[;,\-:!\s]+"
    match = re.split(pattern, i)
    for i in match:
        if i == 'name':
            index_list = match.index('name')
            match_dict['name'] = match[index_list + 1]
        if i.isdigit() and len(i) == 10:
            ls.append(i)
        if i == "birthday":
            index_list = match.index('birthday')
            match_dict['birthday'] = match[index_list + 1][:-1]
    match_dict['phones'] = ls

    return match_dict


def write_txt(book):
    path = "users_inform.txt"
    list = []
    counter = 0
    for i, j in book.items():
        counter += 1
        text = f"№{counter} {j}\n"
        list.append(text)
    with open(path, 'w') as fh:
        for i in list:
            fh.write(f'{i}')


def write_congratulation_date(book):
    path = "congratulation_date.txt"
    counter = 0
    ls = AddressBook.get_upcoming_birthdays(book)
    with open(path, 'w') as fh:
        for i in ls:
            counter += 1
            fh.write(f"№{counter} {i['name'].capitalize()} congratulation date: {i['congratulation_date']} \n")
