import numpy as np


def landmarks_to_numpy(landmarks, get_z=True):
    if get_z:
        np_landmarks = np.empty((21, 3))
    else:
        np_landmarks = np.empty((21, 2))

    for index, landmark in enumerate(landmarks):
        if get_z:
            np_landmarks[index, :] = np.array([landmark.x, landmark.y, landmark.z])
        else:
            np_landmarks[index, :] = np.array([landmark.x, landmark.y])

    return np_landmarks


def normalized_landmarks(landmarks):
    base_x, base_y = landmarks[0, 0], landmarks[0, 1]
    landmarks_norm = landmarks - np.array([base_x, base_y])
    landmarks_norm /= np.linalg.norm(landmarks_norm)
    return landmarks_norm
