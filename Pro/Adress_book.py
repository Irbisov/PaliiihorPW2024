from collections import UserDict
from datetime import datetime, timedelta, date
from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def __getitem__(self):
        pass

    def __str__(self):
        return str(self.value)


class Name(Field):

    def __getitem__(self):
        return self.value


class Phone(Field):
    def phone(self):
        if len(self.value) == 10 and self.value.isdigit():
            return Phone(self.value)
        else:
            print(
                f"Phone number {self.value} not correct. A class for storing a phone number. Has format validation "
                f"(10 digits).")

    def __getitem__(self):
        return self.value


class Birthday(Field):
    def __getitem__(self):
        try:
            data_birthday = (datetime.strptime(self.value, "%d.%m.%Y").date()).strftime("%d.%m.%Y")
            self.value = data_birthday
            return self.value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        message = "Phone number has twins."
        if bool(Phone(phone).phone()):
            for i in self.phones:
                if str(i) == str(Phone(phone).phone()):
                    return print(message)
            self.phones.append(Phone(phone).phone())

    def add_birthday(self, user_birthday):
        self.birthday = Birthday(user_birthday)
        return self.birthday

    def remove_phone(self, phone):
        try:
            self.phones.remove(Phone(phone).phone())
        except ValueError:
            print(f'Phone number {phone} for remove not exist')

    def edit_phone(self, old_phone, new_phone):
        old_phone = Phone(old_phone).phone()
        new_phone = Phone(new_phone).phone()
        for i in self.phones:
            if str(i) == str(old_phone):
                index = self.phones.index(i)
                self.phones.remove(i)
                self.phones.insert(index, new_phone)
                return None

        print(f'Phone number {old_phone} for edit not exist')

    def find_phone(self, phone):
        if Phone(phone).phone() in self.phones:
            return phone
        return None

    def __str__(self):
        if self.birthday != None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}."
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}."


class AddressBook(UserDict):

    def add_record(self, contact_name: Record):
        self.data[contact_name.name.value] = contact_name

    def find(self, name) -> Record:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        del self.data[name]

    def __string_to_date(self, date_string):
        return datetime.strptime(date_string, "%d.%m.%Y").date()

    def __date_to_string(self, date):
        return date.strftime("%d.%m.%Y")

    def __find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def __adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.__find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        next_year = datetime(year=2025, month=12, day=30).year
        for name, inform in self.data.items():
            birthday_this_year = self.__string_to_date(inform.birthday.value).replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = self.__string_to_date(inform.birthday.value).replace(year=next_year)
            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = self.__adjust_for_weekend(birthday_this_year)
                congratulation_date_str = self.__date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": inform.name.value, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays
