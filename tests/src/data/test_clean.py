from unittest import TestCase
from pandas import DataFrame
from numpy import ndarray, matrix

from src.data.clean import (
    find_correct_names,
    _cluster_and_label,
    _build_distance_matrix
)


class TestClusterAndLabel(TestCase):

    def runTest(self):
        pass

    def setUp(self):
        self.df = DataFrame(
            [
                ["aaa", "zzz", 2],
                ["aab", "zzz", 1],
                ["ddd", "xxx", 2],
                ["dde", "xxx", 2],
                ["fff", "yyy", 1]
            ],
            columns=["firstname", "lastname", "count"]
        )
        self.df["name"] = self.df["lastname"] + self.df["firstname"]

    def tearDown(self):
        del self.df

    def test_cluster_labels(self):
        expected = [0, 0, 1, 1, 2]
        result = _cluster_and_label(self.df, column="name", label="label")
        result = list(result["label"])
        self.assertEqual(result, expected)


class TestBuildDistanceMatrix(TestCase):

    def setUp(self):
        self.df = DataFrame(
            [
                ["aaa", "zzz", 1],
                ["aab", "zzz", 1],
                ["abb", "zzz", 1],
                ["bbb", "zzz", 1]
            ],
            columns=["firstname", "lastname", "count"]
        )
        self.df["name"] = self.df["lastname"] + self.df["firstname"]

    def tearDown(self):
        del self.df

    def runTest(self):
        pass

    def test_default_params(self):
        expected = matrix(
            [
                [0, 1, 2, 3],
                [1, 0, 1, 2],
                [2, 1, 0, 1],
                [3, 2, 1, 0]
            ]
        )
        dist = _build_distance_matrix(self.df)
        result = dist == expected
        self.assertTrue(
            result.all(),
            "\n{0} \n!=\n {1}".format(expected, dist)
        )

    def test_width_zero(self):
        expected = matrix(
            [
                [0, 10, 10, 10],
                [10, 0, 10, 10],
                [10, 10, 0, 10],
                [10, 10, 10, 0]
            ]
        )
        dist = _build_distance_matrix(self.df, width=0, default_dist_value=10)
        result = dist == expected
        self.assertTrue(
            result.all(),
            "\n{0} \n!=\n {1}".format(expected, dist)
        )

    def test_width_one(self):
        expected = matrix(
            [
                [0, 1, 10, 10],
                [1, 0, 1, 10],
                [10, 1, 0, 1],
                [10, 10, 1, 0]
            ]
        )
        dist = _build_distance_matrix(self.df, width=1, default_dist_value=10)
        result = dist == expected
        self.assertTrue(
            result.all(),
            "\n{0} \n!=\n {1}".format(expected, dist)
        )

