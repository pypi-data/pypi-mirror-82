"""
Created Wednesday August 19 2020 18:56 +0700

@author: arunwpm, haimoshri
"""
import os

from mitnewsclassify import download

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model

import torch
import numpy as np
from transformers import DistilBertModel, DistilBertTokenizer

import traceback
import csv
import pickle

device = "cuda:0" if torch.cuda.is_available() else "cpu"
device = torch.device(device)

def loadcsv(filename):
    with open(filename, newline='') as f: 
        return list(csv.reader(f))

tokenizer = None
bert = None
ld = None
id2tag = {}

def initialize( ldloc = 'labels_dict_distilbert.csv', #name of the labels dictionary
                id2tagloc = 'nyt-theme-tags.csv' #name of the conversion table from tag id to tag name for NYTcorpus
                ):
    global tokenizer
    global bert
    global ld
    global id2tag

    # warning
    print("WARNING This model will consume a lot of memory, which can render your computer unusable. Please make sure that you have sufficient memory!")

    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased")
    bert = DistilBertModel.from_pretrained('distilbert-base-cased').to(device)

    # get package directory
    pwd = os.path.dirname(os.path.abspath(__file__))
    pwd = pwd + "/data/distilbert/"
    if (not os.path.isdir(pwd)):
        answer = input("The model files have not been downloaded and the methods will not work. Would you like to download them? [y/n] ")
        if answer == 'y':
            download.download('distilbert')

    print("Initializing...")
    
    # initialize the matrix index -> tag id file and the tag id -> tag name file
    # with open(pwd + ldloc, "rb") as ldin:
        # ld = pickle.load(ldin)
    ld = loadcsv(pwd + ldloc)
    ld = {int(row[0]):row[1] for row in ld}
    id2tag_table = loadcsv(pwd + id2tagloc)
    for row in id2tag_table:
        if row == []:
            continue
        id2tag[row[1]] = row[2]
    print("Miscellaneous...")

def getfeatures(txt):
    if (ld is None):
        initialize()
    with torch.no_grad():
        encoded_dict = tokenizer([txt], add_special_tokens=True, pad_to_max_length=True, max_length=300, return_tensors="pt", return_attention_mask=True)
        result = encoded_dict['input_ids']
        attention_mask = encoded_dict['attention_mask']
        output = bert(input_ids=encoded_dict['input_ids'].to(device), attention_mask=encoded_dict['attention_mask'].to(device))
        output = torch.mean(output[0], 1).detach()
        vec1 = output.cpu()
    # print(vec1)

    return vec1

def free():
    global tokenizer
    del tokenizer
    global bert
    del bert

if __name__ == "__main__":
    while True:
        txt = input("Enter text: ")
        gettags(txt)