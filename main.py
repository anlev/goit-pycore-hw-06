from collections import UserDict


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
    pass


class Phone(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits (0-9).")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        self._value = value


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number: str):
        phone = self.find_phone(phone_number)
        if phone is not None:
            raise ValueError("Phone number already exists.")
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number: str):
        phone = self.find_phone(phone_number)
        if phone is None:
            raise ValueError("Phone number not found.")
        self.phones.remove(phone)

    def find_phone(self, phone_number: str):
        return next((phone for phone in self.phones if phone.value == phone_number), None)

    def edit_phone(self, phone_number: str, new_phone_number: str):
        phone = self.find_phone(phone_number)
        if phone is None:
            raise ValueError("Phone number not found.")
        phone.value = new_phone_number


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        self.data.pop(name)


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    print("--------")

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    john.remove_phone("5555555555")
    print(john)

    print("--------")

    found_phone = john.find_phone("1112223333")
    print(f"{john.name}: {found_phone}")  # Виведення: 1112223333

    book.delete("Jane")
