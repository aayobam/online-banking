import random
from datetime import datetime


def generate_card_number():
    card_number = random.randint(000000000000, 999999999999)
    return card_number


def generate_cvv():
    cvv = random.randint(000, 9999999)
    return cvv


def generate_expiry_date():
    expiry_date = datetime.now().year + 3
    return expiry_date
