# -*- coding: utf-8 -*-

import pickle

def main():
    graph = {
        "Computer science": ["Computational complexity theory", "Theory of computation"],
        "Computational complexity theory": ["Theory of computation"],
        "Theory of computation": []
    }

    pickle.dump(graph, open('data/mock.pkl', 'wb'), -1)

if __name__ == "__main__":
    main()
