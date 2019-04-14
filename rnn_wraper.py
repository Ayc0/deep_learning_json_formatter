#!/usr/bin/env python3
import os
import json
import sys
import unicodedata
import random
import json
import torch

from random_json import generate_random_json

# Two categories: well-formatted (0) and not well-formatted (1)
n_categories = 2
categories = ["pretty", "raw"]
# Alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + \
    "1234567890" + "!,.:;?" + r""" \"#$%&'()*+-/<=>@[]^_`{|}~"""


def to_ascii(s: str):
    # From https://stackoverflow.com/a/518232/2809427
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn' and c in alphabet)


def random_training_pair():
    category = random.randint(0, 1)
    obj = generate_random_json()
    if category == 0:
        # Format the JSON
        obj = json.dumps(json.loads(obj), indent=4)
    return category, obj


def category_tensor(category):
    tensor = torch.zeros(1, n_categories)
    index = categories.index(category)
    tensor[0][index] = 1
    return tensor


def input_tensor(obj):
    sample = str(obj)
    tensor = torch.zeros(len(sample), 1, len(alphabet))
    for i in range(len(sample)):
        char = sample[i]
        tensor[i][0][alphabet.find(char)] = 1
    return tensor


def target_tensor(obj):
    # Weird stuff in original version
    sample = str(obj)
    indexes = [alphabet.find(sample[i]) for i in range(1, len(sample))]
    indexes.append(len(alphabet))  # This corresponds to the EOS/EOF character
    return torch.LongTensor(indexes)


def random_example():
    category, obj = random_training_pair()
    cat_tensor = category_tensor(category)
    in_tensor = input_tensor(obj)
    tgt_tensor = target_tensor(obj)
    return cat_tensor, in_tensor, tgt_tensor
