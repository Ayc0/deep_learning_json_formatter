from random import random, randrange, choice
import json

default_max_depth = 2
default_max_num = 1 << 16
default_max_string_length = 25
default_max_array_length = 10
default_max_object_keys = 10
default_max_key_length = 10

number = "0123456789"
letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
point = "!,.:;?"
other = r""" \"#$%&'()*+-/<=>@[]^_`{|}~
"""
full_alphabet = number + letter + point + other


def choose_one(choices):
    return choice(choices)


def generate_random_boolean():
    return choose_one([True, False])


def generate_random_number(max_num=default_max_num):
    number = random() * max_num
    is_integer = generate_random_boolean()
    is_negative = generate_random_boolean()

    if is_integer:
        number = int(number)
    if is_negative:
        number = -number

    return number


def generate_random_string(max_string_length=default_max_string_length):
    choices = [
        "number",
        "number",
        "number",
        "number",
        "letter",
        "letter",
        "letter",
        "letter",
        "letter",
        "letter",
        "letter",
        "letter",
        "letter",
        "letter",
        "letter",
        "point",
        "other",
    ]
    length = randrange(max_string_length)
    string = ""

    for _ in range(length):
        choice = choose_one(choices)
        if choice == "number":
            alphabet = number
        elif choice == "letter":
            alphabet = letter
        elif choice == "point":
            alphabet = point
        else:
            alphabet = other
        string += choose_one(alphabet)
    return string


def generate_random_array(
    max_depth=default_max_depth,
    max_array_length=default_max_array_length,
    max_key_length=default_max_key_length,
    max_object_keys=default_max_object_keys,
):
    length = randrange(max_array_length)

    array = []
    for _ in range(length):
        array.append(generate_random_json(max_depth - 1, max_array_length=max_array_length))

    return array


def generate_random_key_name(max_key_length=default_max_key_length):
    key_length = 1 + randrange(max_key_length)
    random_string = generate_random_string()
    return random_string[:key_length]


def generate_random_object(
    max_depth=default_max_depth,
    max_array_length=default_max_array_length,
    max_key_length=default_max_key_length,
    max_object_keys=default_max_object_keys,
):
    key_count = randrange(max_object_keys)

    object = {}
    for _ in range(key_count):
        key = generate_random_key_name(max_key_length=max_key_length)
        object[key] = generate_random_json(max_depth - 1, max_key_length=max_key_length)

    return object


def format_json(obj):
    return json.dumps(obj, indent=4)


def generate_random_json(
    max_depth=default_max_depth,
    max_array_length=default_max_array_length,
    max_key_length=default_max_key_length,
    max_object_keys=default_max_object_keys,
):
    choices = [
        "number",
        "string",
        "boolean",
        "array",
        "array",
        "array",
        "array",
        "object",
        "object",
        "object",
        "object",
        "none",
    ]
    if max_depth == 0:
        choices = ["number", "string", "boolean", "none"]

    choice = choose_one(choices)

    if choice == "number":
        json = generate_random_number()
    if choice == "string":
        json = generate_random_string()
    if choice == "boolean":
        json = generate_random_boolean()
    if choice == "array":
        json = generate_random_array(
            max_depth=max_depth,
            max_array_length=max_array_length,
            max_key_length=max_key_length,
            max_object_keys=max_object_keys,
        )
    if choice == "object":
        json = generate_random_object(
            max_depth=max_depth,
            max_array_length=max_array_length,
            max_key_length=max_key_length,
            max_object_keys=max_object_keys,
        )
    if choice == "none":
        json = None

    return json
