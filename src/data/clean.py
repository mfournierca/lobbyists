import pandas
import numpy
import Levenshtein
from sklearn import cluster
import Levenshtein


def find_correct_names(names):
    """Given a list of (lastname, firstname, frequency) tuples find the correct
    spelling of each name.

    We accomplish this in 2 steps:

    - Cluster the names so that mispellings are in the same cluster
    - Take the most frequent spelling from each cluster and consider it correct
    """

    df = pandas.DataFrame(names, columns=["lastname", "firstname", "count"])

    # distance will be measured off of full name
    df["name"] = df["lastname"] + df["firstname"]

    # remove non-ascii characters, sklearn crashes
    df["name"] = df["name"].apply(
        lambda x: "".join([i for i in x if 0 < ord(i) < 127])
    )

    # build distance matrix
    dist = _build_distance_matrix(df)

    # find labels
    dbscan = cluster.DBSCAN(eps=3, metric="precomputed", min_samples=1)
    labels = dbscan.fit_predict(dist)
    df["label"] = labels

    # find the index of the max count within each label
    correct = df.groupby("label")["count"].idxmax()

    # join with the original dataframe

    return df


def _build_distance_matrix(
        df,
        col="name",
        width=10,
        default_dist_value=10000
    ):
    dist = numpy.ndarray((len(df), len(df)))
    dist.fill(default_dist_value)
    for i, n in enumerate(df[col]):
        if i - width <= 0:
            lower = 0
        else:
            lower = i - width

        if i + width >= len(df[col]):
            upper = len(df[col]) - 1
        else:
            upper = i + width

        for j, m in enumerate(df[col][lower:upper + 1]):
            pos = j + lower
            d = Levenshtein.distance(n, m)
            dist[i][pos] = d

    return dist
