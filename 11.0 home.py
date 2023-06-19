from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not new_value.isdigit():
            raise ValueError("Phone number must contain only digits")
        self.__value = new_value

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if new_value is not None:
            try:
                datetime.strptime(new_value, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Birthday must be in the format 'dd-mm-yyyy'")
        self.__value = new_value

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def days_to_birthday(self):
        if not self.birthday.value:
            return None
        current_date = datetime.now()
        birthday_date = datetime.strptime(self.birthday.value, "%d-%m-%Y").replace(year=current_date.year)
        if birthday_date < current_date:
            birthday_date = birthday_date.replace(year=current_date.year + 1)
        delta = birthday_date - current_date
        return delta.days + 1

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n=1):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i+n]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            result = "No user with given name"
        except ValueError as e:
            result = str(e)
        except IndexError:
            result = "Enter user name"
        return result
    return inner

def hello_handler():
    return "How can I help you?"

@input_error
def add_handler(command):
    parts = command.split()
    name_str = parts[1]
    phone_str = parts[2]
    try:
      birthday_str = parts[3]
      birthday = Birthday(birthday_str)
    except IndexError:
      birthday_str = None
      birthday = Birthday()
    
    name = Name(name_str)
    phone = Phone(phone_str)
    
    record = Record(name=name, phone=phone, birthday=birthday)
    
    address_book.add_record(record)
    
    if birthday_str is None:
      return f"User {name.value} with phone number {phone.value} was added"
    
    return f"User {name.value} with phone number {phone.value} and birthday {birthday.value} was added"

@input_error
def change_handler(command):
    parts = command.split()
    
    name_str = parts[1]
    
    name = Name(name_str)
    
    record = address_book.data[name.value]
    
    for part in parts[2:]:
      if part.startswith("+"):
          phone_str = part
          phone = Phone(phone_str)
          record.add_phone(phone)
      else:
          birthday_str = part
          birthday = Birthday(birthday_str)
          record.birthday=birthday
def phone_handler(command):
  name_str=command.split()[1]
  name=Name(name_str)
  record=address_book.data[name.value]
  phones=[phone.value for phone in record.phones]
  return "\\n".join(phones)

def show_all_handler():
  result=[]
  for page in address_book.iterator(2):
      for record in page:
          name=record.name.value
          phones=[phone.value for phone in record.phones]
          result.append(f"{name}: {', '.join(phones)}")
  return "\\n".join(result)

def exit_handler():
  return "Good bye!"

HANDLERS={
  "hello": hello_handler,
  "add": add_handler,
  "change": change_handler,
  "phone": phone_handler,
  "show all": show_all_handler,
  "good bye": exit_handler,
  "close": exit_handler,
  "exit": exit_handler
}

address_book=AddressBook()

@input_error
def handle_command(command):
  command=command.lower()
  for key in HANDLERS:
      if command.startswith(key):
          handler=HANDLERS[key]
          return handler(command)
  return "Unknown command"

def main():
  while True:
      command=input()
      result=handle_command(command)
      print(result)
      if result=="Good bye!":
          break

if __name__=="__main__":
    main()
