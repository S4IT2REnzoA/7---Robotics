from cv2 import sqrt


def manhattan_dist(p1,p0):
    return abs(p1[1] - p0[1]) + abs(p1[0] - p0[0])

def euclidean_dist(p1,p0):
    return sqrt((p1[1] - p0[1])**2 + (p1[0] - p0[0])**2)