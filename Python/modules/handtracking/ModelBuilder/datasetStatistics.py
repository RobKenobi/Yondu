import numpy as np
import os
# Hand signs dictionary
signs = {
    "o": 0,  # Open hand
    "c": 1,  # Closed hand
    "i": 2,  # index up
    "p": 3,  # thumb up
    "v": 4,  # index and middle finger up
    "k": 5,  # index and thumb joined
}

# Hand signs description dictionary
signs_description = {
    "o": "Open hand",
    "c": "Closed hand",
    "i": "index up",
    "p": "thumb up",
    "v": "index and middle finger up",
    "k": "index and thumb joined"
}

sign_nb = dict()
for key in signs:
    sign_nb[signs[key]] = signs_description[key]


def show_statistics(label, handedness):
    count = np.bincount(label)
    print(f"\n On {handedness} hand : ")
    for index, sign in enumerate(count):
        print(f" - Nb: {sign} \t{sign_nb[index]}")
    print(f"TOTAL : {len(label)}")


dataset_left = np.loadtxt("dataset_left.csv", delimiter=',')
dataset_right = np.loadtxt("dataset_right.csv", delimiter=',')

label_left = dataset_left[:, 0].astype('int')
label_right = dataset_right[:, 0].astype('int')

show_statistics(label_left, "left")
show_statistics(label_right, "right")
