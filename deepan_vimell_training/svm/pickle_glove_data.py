import pickle
from parse_data import get_50_w2v, get_100_w2v, get_200_w2v, get_300_w2v


def pickle_data(w2v, dim):
    filename = "glove_files/" + str(dim) + ".pickle"
    with open(filename, "wb+") as f:
        pickle.dump(w2v, f)
    print("pickled glove file dim = ", dim)


w2v_50 = get_50_w2v()
pickle_data(w2v_50, 50)

w2v_100 = get_100_w2v()
pickle_data(w2v_100, 100)

w2v_200 = get_200_w2v()
pickle_data(w2v_200, 200)

w2v_300 = get_300_w2v()
pickle_data(w2v_300, 300)
