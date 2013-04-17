# -*- coding: utf-8 -*-

from lib.graph import *
import pickle

def main():
    graph = Graph(
                Node({"title": "Foo"}, [
                    Node({"title": "Foo1"}, []),
                    Node({"title": "Foo2"}, [
                            Node({"title": "Bar"}, [])
                        ])
                ])
            )

    pickle.dump(graph, open('data/mock.pkl', 'wb'), -1)

if __name__ == "__main__":
    main()
