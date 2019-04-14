#!/usr/bin/env python3
import os
import json
import sys
import unicodedata
import random
import json
import time
import math
import matplotlib.pyplot as plt
import torch

from random_json import generate_random_json, format_json, full_alphabet
from rnn import *

# Two categories: well-formatted (0) and not well-formatted (1)
n_categories = 2
categories = ["pretty", "raw"]
# Alphabet
n_char = len(full_alphabet) + 1  # Include EOS as a character

# Learning parameters
criterion = nn.NLLLoss()
learning_rate = 0.0005


# def to_ascii(s: str):
#     # From https://stackoverflow.com/a/518232/2809427
#     return ''.join(c for c in unicodedata.normalize('NFD', s)
#                    if unicodedata.category(c) != 'Mn' and c in full_alphabet)


def random_training_pair():
    index = random.randint(0, n_categories - 1)
    category = categories[index]
    obj = generate_random_json()
    if category == 0:
        # Format the JSON
        obj = format_json(obj)
    return category, obj


def category_tensor(category):
    tensor = torch.zeros(1, n_categories)
    index = categories.index(category)
    tensor[0][index] = 1
    return tensor


def input_tensor(obj):
    sample = str(obj)
    tensor = torch.zeros(len(sample), 1, n_char)
    for i in range(len(sample)):
        char = sample[i]
        tensor[i][0][full_alphabet.find(char)] = 1
    return tensor


def target_tensor(obj):
    sample = str(obj)
    indexes = [full_alphabet.find(sample[i]) for i in range(1, len(sample))]
    indexes.append(n_char - 1)  # This corresponds to the EOS character
    return torch.LongTensor(indexes)


def random_example():
    category, obj = random_training_pair()
    cat_tensor = category_tensor(category)
    in_tensor = input_tensor(obj)
    tgt_tensor = target_tensor(obj)
    return cat_tensor, in_tensor, tgt_tensor


def time_elapsed(origin):
    seconds = time.time() - origin
    minutes = math.floor(seconds / 60)
    seconds -= minutes * 60
    return "{:d}m {:d}s".format(minutes, seconds)


def train(cat_tensor, in_tensor, tgt_tensor):
    tgt_tensor.unsqueeze_(-1)
    hidden = rnn.init_hidden()
    rnn.zero_grad()

    loss = 0
    for i in range(in_tensor.size(0)):
        out, hidden = rnn(cat_tensor, in_tensor[i], hidden)
        l = criterion(out, tgt_tensor[i])
        loss += l
    loss.backward()

    for p in rnn.parameters():
        p.data.add_(-learning_rate, p.grad.data)

    return out, loss.item() / in_tensor.size(0)


def train_nn():
    n_iters = 100000
    print_interval = 500
    plot_interval = 500
    losses_list = []
    interval_loss = 0  # Reset every plot_every iters

    begin = time.time()

    # Train the network
    for iter in range(1, n_iters + 1):
        out, loss = train(*random_example())
        interval_loss += loss

        if iter % print_interval == 0:
            print("{}\t{:d}\t{:.3f}".format(time_elapsed(begin), iter, loss))
        if iter % plot_interval == 0:
            losses_list.append(interval_loss / plot_interval)
            interval_loss = 0

    # Plot
    plt.figure()
    plt.plot(losses_list)
    plt.show()


rnn = RNN(n_char, 128, 2048)
train_nn()
