import numpy as np

# Hand signs dictionary
signs = {
    "o": 0,  # Open hand
    "c": 1,  # Closed hand
    "i": 2,  # index up
    "f": 3,  # middle finger up
    "v": 4,  # index and middle finger up
    "e": 5,  # thumb and pinky up
    "s": 6,  # thumb, index and pinky up
    "u": 7,  # index and pinky up
    "k": 8,  # index and thumb joined
    "t": 9  # italian sign
}

# Hand signs description dictionary
signs_description = {
    "o": "Open hand",
    "c": "Closed hand",
    "i": "index up",
    "f": "middle finger up",
    "v": "index and middle finger up",
    "e": "thumb and pinky up",
    "s": "thumb, index and pinky up",
    "u": "index and pinky up",
    "k": "index and thumb joined",
    "t": "italian sign"
}

sign_nb = dict()
for key in signs:
    sign_nb[signs[key]] = signs_description[key]
print(sign_nb)


def show_statistics(label, handedness):
    count = np.bincount(label)
    print(f"\n On {handedness} hand : ")
    for index, sign in enumerate(count):
        print(f" - Nb: {sign} \t{sign_nb[index]}")
    print(f"TOTAL : {len(label)}")


data_left = np.load("data_left.npy")
label_left = np.load("label_left.npy")
data_right = np.load("data_right.npy")
label_right = np.load("label_right.npy")

show_statistics(label_left, "left")
show_statistics(label_right, "right")
