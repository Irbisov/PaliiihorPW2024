from Adress_book import AddressBook, Record
import pickle
from parser_txt import read_txt, write_txt, write_congratulation_date
from Comands import comands


def input_error(function):
    match function.__name__:
        case "add_contact":
            def inner(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except (TypeError, ValueError):
                    return print("Func add, give me name and phone please.")
        case "parse_input":
            def inner(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except (ValueError, TypeError):
                    return print("Func input, give any command .")
        case "change_username_phone":
            def inner(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except (TypeError, ValueError):
                    return print("Func change_phone, give me name and phone please.")
        case "phone_username":
            def inner(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except (TypeError, ValueError, IndexError):
                    return print("Func phone, give me name please.")
        case "add_birthday":
            def inner(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except (TypeError, ValueError, IndexError):
                    return print("Func add_birthday, give me inform please.")
        case "show_birthday":
            def inner(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except (TypeError, ValueError, IndexError):
                    return print("Func show_birthday, give me inform please.")
        case _:
            return print("Func not found")
    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_username_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        message = "Contact not found."
        return print(message)
    else:
        record.edit_phone(old_phone, new_phone)


@input_error
def phone_username(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        message = "Contact not found."
        return print(message)
    else:
        return print(f"Name: {record.name.value}, phones: {'; '.join(p.value for p in record.phones)}.")


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        message = "Contact not found."
        return print(message)
    else:
        record.add_birthday(birthday)


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        message = "Contact not found."
        return print(message)
    else:
        return print(f"Name: {record.name}, birthday: {record.birthday}.")


def birthday(book: AddressBook):
    for i in AddressBook.get_upcoming_birthdays(book):
        print(i)


def all(book: AddressBook):
    counter = 0
    for i, j in book.items():
        counter += 1
        print(f"№{counter} {j}")


def delete(args, book: AddressBook):
    name, *_ = args
    book.delete(name)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    print(comands)
    book = load_data()
    user_txt = read_txt()
    if user_txt:
        for i in user_txt:
            book.add_record(i)
    print("Welcome to the assistant bot New Adress book!")
    while True:
        user_input = input("Enter a command: ")
        if user_input:
            command, *args = parse_input(user_input)
            write_txt(book)
            save_data(book)
            if command in ["close", "exit", ]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                add_contact(args, book)
            elif command == "change":
                change_username_phone(args, book)
            elif command == "phone":
                phone_username(args, book)
            elif command == "all":
                all(book)
            elif command == "add_birthday":
                add_birthday(args, book)
            elif command == "show_birthday":
                show_birthday(args, book)
            elif command == "birthdays":
                birthday(book)
                write_congratulation_date(book)
            elif command == "delete":
                delete(args, book)
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
