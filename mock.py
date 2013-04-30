# -*- coding: utf-8 -*-

import pickle

def main():
    graph = {
        "Computer science": set(["Computational complexity theory", "Theory of computation", "Abstract algebra"]),
        "Computational complexity theory": set(["Complexity theory", "Lambda calculus"]),
        "Abstract algebra": set(["Von Newman"]),
        "Theory of computation": set()
    }

    pickle.dump(graph, open('data/mock.pkl', 'wb'), -1)

if __name__ == "__main__":
    main()
