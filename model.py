import torch
import torch.nn as nn
import torch.nn.functional as F

from torch import optim
from torch.utils.data import Dataset, DataLoader

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

from extract import extract
from crop import crop

import warnings
warnings.filterwarnings("ignore")

# load model :

# En utilisant Sequential(), créer un modèle avec l'architecture susmentionnée
input_size = 32
hidden_sizes = [100, 70, 25]
output_size = 10
model = nn.Sequential(nn.Conv2d(input_size, hidden_sizes[0], kernel_size=3),
                      nn.ReLU(), nn.Linear(hidden_sizes[0], hidden_sizes[1]),
                      nn.ReLU(), nn.Linear(hidden_sizes[1], output_size),
                      nn.LogSoftmax(dim=1))


# Créer une classe qui hérite de nn.Module et redéfinir le constructeur ainsi que la méthode forward
class myNN(nn.Module):
    def __init__(self):
        super(myNN, self).__init__()
        self.fc1 = nn.Linear(32, 100)
        self.fc2 = nn.Linear(100, 70)
        self.fc3 = nn.Linear(70, 25)
        self.fc4 = nn.Linear(25, 10)
        #self.dropout = nn.Dropout(p=0.5)
    def forward(self, x):
        x = x.view(-1, 32)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


my_model = myNN()
my_model.load_state_dict(torch.load('./model-80-91'))


def apply_model(img):
    val = extract(img)
    hehe = my_model(torch.FloatTensor(val))
    return hehe.data.max(1, keepdim=True)[1].item()
