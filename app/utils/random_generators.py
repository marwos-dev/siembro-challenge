import random
import string

FIRST_NAMES = [
    "Lucas", "Mateo", "Thiago", "Benjamin", "Emma", "Olivia", "Mia",
    "Sofia", "Liam", "Noah", "Ethan", "Ava", "Amelia", "Harper"
]

LAST_NAMES = [
    "Gonzalez", "Rodriguez", "Fernandez", "Lopez", "Martinez",
    "Perez", "Sanchez", "Gomez", "Diaz", "Torres"
]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_email(unique_id: int):
    first = ''.join(random.choices(string.ascii_lowercase, k=5))
    last = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"{first}.{last}.{unique_id}@mail.com"
