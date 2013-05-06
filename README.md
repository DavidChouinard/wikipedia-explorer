Wikipedia Explorer
=================

This builds a directed graph representation of Wikipedia articles, with links between articles represented as edges on the graph. Final project for Harvard's [CS51](http://cs51.seas.harvard.edu/).

Usage
------------

For all scripts, usage instructions is available with the `--help` switch.

### Crawler

The **crawler** queries the Wikipedia API to build a graph representation for a particular Wikipedia category. It can be invoked as follows:

```
python crawler.py "History of computer science"
```

A second argument can also be provided to specific where to output the dataset file. If no argument is provided, the resulting graph is outputed to `data/wikipedia.pkl`.

### Shorthest path

The shortest path script takes a graph dataset and two article names to compute the shortest path (if any) between them, as follows:

```
python shortest_path.py data/wikipedia.pkl "History of computer science" "Source code"
```

By default, the script will use breadth-first search to run the computation. The `-n` or `-d` switch can be used to force usage of the naive algorithm or Dijkstra's algorithm (with unit weights), respectively.

### Popular articles

The most popular articles (ie. the ones with most incoming links) can be found like so, with the number being how many of the most popular articles you want to print out:

```
python popular.py data/wikipedia.pkl 10 
```

An optional second argument can be passed to specify the number of results to return (defaults to 10).

### Clustering

The following partitions the graph into clusters:

```
python cluster.py data/wikipedia.pkl
```

Tests
------------

Unit tests can be executed by running:

```
python test.py
```
