"""
Entry point
"""

import pickle
from collections import defaultdict
from src.handlers import *
from src.entities import AddressBook

class AddressBook:
    def __init__(self):
        self.data = {}
        self.notes = NoteBook()


def save_data(book: AddressBook, filename: str="addressbook.pkl") -> None:
    """
    Save AddressBook with all its object hierarchy to file in binary format
    "filename" may be empty or None to indicate that no saving is necessary.
    """
    if not filename:
        return
    try:
        with open(filename, "wb") as file:
            pickle.dump(book, file)
    except IOError as e:
        print(f"Error saving state: {e}")

def load_data(filename: str="addressbook.pkl") -> AddressBook:
    """
    Load AddressBook previously saved by "save_data" function
    """
    # empty str or None indicate to start with empty AddressBook
    if not filename:
        return AddressBook()
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (IOError, EOFError) as e:
        # EOFError is for wrong file format
        print(f"Warning: unable to load state from '{filename}': {e}")
        return AddressBook()

def main(start_empty: bool = False, filename: str = "addressbook.pkl"):
    """
    Main loop for bot

    "start_empty" flag indicates to start with empty AddressBook
        and to use filename to save final state only.
    
    "filename" is a path to file to save database state. 
        None or empty string would indicate to work in memory only. 
    """

    if start_empty:
        contacts = load_data(None)
    else:
        contacts = load_data(filename)

    # command handlers

    def default_handler():
        def inner(*args, **kwargs):
            return "Invalid command."
        return inner

    # all handlers should take 2 arguments - args list and contacts dictionary
    handlers = defaultdict(default_handler, {
        "hello": lambda x,y: "How can I help you?",
        "close": lambda x,y: "Good bye!",
        "exit": lambda x,y: "Good bye!",
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
    })

    print("Welcome to the assistant bot!")

    # main loop
    command = ""
    while command not in ["close", "exit"]:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        print(handlers[command](args, contacts))

    save_data(contacts, filename)


if __name__ == "__main__":
    main()

    ## Note and comment
    class Note:
     def __init__(self, text: str, tags=None):
        self.text = text
        self.tags = tags or []

    def __str__(self):
        tags_str = f" [tags: {', '.join(self.tags)}]" if self.tags else ""
        return f"{self.text}{tags_str}"


class NoteBook:
    def __init__(self):
        self.notes = []

    def add(self, note: Note):
        self.notes.append(note)

    def delete(self, index: int):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            return True
        return False

    def search_by_tag(self, tag: str):
        return [n for n in self.notes if tag in n.tags]

    def __str__(self):
        if not self.notes:
            return "There are no Notes"
        return "\n".join(f"{i}. {note}" for i, note in enumerate(self.notes))
    
