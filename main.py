import re
from collections import UserDict


PHONE_REGEX = re.compile(r"\d{10}")


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    @Field.value.setter
    def value(self, name):
        if not name:
            raise ValueError("Name cannot be empty.")
        self._value = name


class Phone(Field):
    @Field.value.setter
    def value(self, new_phone_number):
        if not PHONE_REGEX.fullmatch(str(new_phone_number)):
            raise ValueError("Phone number must contain exactly 10 digits.")
        self._value = new_phone_number


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if not phone_obj:
            raise ValueError("Phone number not found.")
        self.phones.remove(phone_obj)

    def edit_phone(self, existing_phone_number, new_phone_number):
        phone_to_edit = self.find_phone(existing_phone_number)
        if not phone_to_edit:
            raise ValueError("Phone number to edit not found.")
        self.phones[self.phones.index(phone_to_edit)] = Phone(new_phone_number)

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        return self.data[name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record with name '{name}' not found.")


def demo_address_book():
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(name, record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # 5555555555

    book.delete("Jane")


if __name__ == "__main__":
    demo_address_book()
