#!/usr/bin/env python3
import torch
import torch.nn as nn

# Number of categories
n_categories = 2


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size

        self.in_to_hidden = nn.Linear(n_categories + input_size + hidden_size, hidden_size)
        self.in_to_out = nn.Linear(n_categories + input_size + hidden_size, output_size)
        self.out_to_out = nn.Linear(hidden_size + output_size, output_size)
        self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, category, input, hidden):
        input_combined = torch.cat((category, input, hidden), 1)
        hidden = self.in_to_hidden(input_combined)
        output = self.in_to_out(input_combined)
        output_combined = torch.cat((hidden, output), 1)
        output = self.out_to_out(output_combined)
        output = self.dropout(output)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)
