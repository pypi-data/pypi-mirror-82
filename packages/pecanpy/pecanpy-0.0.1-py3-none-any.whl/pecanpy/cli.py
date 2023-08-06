"""Command line utility for PecanPy."""

import argparse
import warnings

from gensim.models import Word2Vec
from pecanpy import node2vec
from pecanpy.wrappers import Timer


def parse_args():
    """Parse node2vec arguments."""
    parser = argparse.ArgumentParser(
        description="Run pecanpy, a parallelized, efficient, and accelerated Python implementataion of node2vec")

    parser.add_argument(
        "--input", nargs="?", default="graph/karate.edgelist", help="Input graph path")

    parser.add_argument(
        "--output", nargs="?", default="emb/karate.emb", help="Embeddings path")

    parser.add_argument(
        "--task", nargs="?", default="pecanpy", help="Choose task: (pecanpy, todense)")

    parser.add_argument(
        "--mode",
        nargs="?",
        default="PreComp",
        help="Choose another mode: (SparseOTF, DenseOTF)")

    parser.add_argument(
        "--dimensions",
        type=int,
        default=128,
        help="Number of dimensions. Default is 128.")

    parser.add_argument(
        "--walk-length",
        type=int,
        default=80,
        help="Length of walk per source. Default is 80.")

    parser.add_argument(
        "--num-walks",
        type=int,
        default=10,
        help="Number of walks per source. Default is 10.")

    parser.add_argument(
        "--window-size",
        type=int,
        default=10,
        help="Context size for optimization. Default is 10. Support list of values")

    parser.add_argument("--iter", default=1, type=int, help="Number of epochs in SGD")

    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel workers. Default is 8.")

    parser.add_argument(
        "--p", type=float, default=1, help="Return hyperparameter. Default is 1.")

    parser.add_argument(
        "--q", type=float, default=1, help="Inout hyperparameter. Default is 1.")

    parser.add_argument(
        "--weighted",
        dest="weighted",
        action="store_true",
        help="Boolean specifying (un)weighted. Default is unweighted.")
    parser.add_argument("--unweighted", dest="unweighted", action="store_false")
    parser.set_defaults(weighted=False)

    parser.add_argument(
        "--directed",
        dest="directed",
        action="store_true",
        help="Graph is (un)directed. Default is undirected.")
    parser.add_argument("--undirected", dest="undirected", action="store_false")
    parser.set_defaults(directed=False)

    parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Print out training details")
    parser.set_defaults(verbose=False)

    return parser.parse_args()


def read_graph(args):
    """Read input network to memory.

    Depending on the mode selected, reads the network either in CSR representation
        (PreComp and SparseOTF) or numpy matrix (DenseOTF).

    """
    fp = args.input
    output = args.output
    p = args.p
    q = args.q
    workers = args.workers
    verbose = args.verbose
    weighted = args.weighted
    directed = args.directed
    mode = args.mode
    task = args.task

    if task == "todense":
        g = node2vec.DenseGraph()
        g.read_edg(fp, weighted, directed)
        g.save(output)
        exit()
    elif task != "pecanpy":
        raise ValueError(f"Unknown task: {repr(task)}")

    if mode == "PreComp":
        g = node2vec.PreComp(p, q, workers, verbose)
        g.read_edg(fp, weighted, directed)
    elif mode == "SparseOTF":
        g = node2vec.SparseOTF(p, q, workers, verbose)
        g.read_edg(fp, weighted, directed)
    elif mode == "DenseOTF":
        g = node2vec.DenseOTF(p, q, workers, verbose)
        if fp.endswith(".npz"):
            g.read_npz(fp, weighted, directed)
        else:
            g.read_edg(fp, weighted, directed)
    else:
        raise ValueError(f"Unkown mode: {repr(mode)}")

    return g


def learn_embeddings(args, walks):
    """Learn embeddings by optimizing the Skipgram objective using SGD."""
    model = Word2Vec(
        walks,
        size=args.dimensions,
        window=args.window_size,
        min_count=0,
        sg=1,
        workers=args.workers,
        iter=args.iter,
    )
    warnings.filterwarnings("ignore")  # disable warning from smart_open used by gensim
    model.wv.save_word2vec_format(args.output)


def main_helper(args):
    """Pipeline for representational learning for all nodes in a graph."""

    @Timer("load graph", True)
    def timed_read_graph():
        return read_graph(args)

    @Timer("pre-compute transition probabilities", True)
    def timed_preprocess():
        g.preprocess_transition_probs()

    @Timer("generate walks", True)
    def timed_walk():
        return g.simulate_walks(args.num_walks, args.walk_length)

    @Timer("train embeddings", True)
    def timed_emb():
        learn_embeddings(args=args, walks=walks)

    g = timed_read_graph()
    timed_preprocess()
    walks = timed_walk()
    g = None
    timed_emb()


def main():
    """Command line script."""
    main_helper(parse_args())


if __name__ == "__main__":
    main()
