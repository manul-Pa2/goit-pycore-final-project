from src.handlers.input_error import input_error
from src.entities import AddressBook, Record

@input_error
def add_email(args: list[str], contacts: AddressBook) -> str:
    """
    Adds new email to contacts book object. 
    If contact with such name already exists, adds one more email for that user.
    "args" should contain 2 values.
    """
    name, email = args
    ## if contact already exists, adding one more email for user
    if not name in contacts:
        contacts[name] = Record(name)
    contacts[name].add_email(email)
    return "Contact added."