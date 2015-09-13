from unittest import TestCase
from pandas import DataFrame, Series
from numpy import ndarray, matrix

from src.data.clean import (
    find_correct_names,
    _cluster_and_label,
    _build_distance_matrix
)


class TestFindCorrectNames(TestCase):

    def runTest(self):
        pass

    def setUp(self):
        self.names = [
            ["zzz", "aaa", 2],
            ["zzz", "aab", 1],
            ["xxx", "ddd", 2],
            ["xxx", "dde", 1],
            ["yyy", "fff", 1]
        ]

        self.expected = DataFrame(
            self.names,
            columns=["lastname", "firstname", "count"]
        )
        self.expected["correct_firstname"] = Series(
            ["aaa", "aaa", "ddd", "ddd", "fff"]
        )
        self.expected["correct_lastname"] = Series(
            ["zzz", "zzz", "xxx", "xxx", "yyy"]
        )

    def test_correct_names(self):

        result = find_correct_names(self.names)

        print(self.expected)
        print(result)

        self.assertTrue(
            (
                result["correct_firstname"] ==
                self.expected["correct_firstname"]
            ).all()
        )
        self.assertTrue(
            (
                result["correct_lastname"] ==
                self.expected["correct_lastname"]
            ).all()
        )


class TestClusterAndLabel(TestCase):

    def runTest(self):
        pass

    def setUp(self):
        self.df = DataFrame(
            [
                ["zzz", "aaa", 2],
                ["zzz", "aab", 1],
                ["xxx", "ddd", 2],
                ["xxx", "dde", 2],
                ["yyy", "fff", 1]
            ],
            columns=["lastname", "firstname", "count"]
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
                ["zzz", "aaa", 1],
                ["zzz", "aab", 1],
                ["zzz", "abb", 1],
                ["zzz", "bbb", 1]
            ],
            columns=["lastname", "firstname", "count"]
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

