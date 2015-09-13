from unittest import TestCase
from pandas import DataFrame, Series
from numpy import ndarray, matrix

from src.data.correct_names import (
    find_correct_names,
    _cluster_and_label,
    _build_distance_matrix
)


class TestFindCorrectNames(TestCase):

    def runTest(self):
        pass

    def setUp(self):
        pass

    def test_simple_names(self):
        names = [
            ["zzz", "aaa", 2],
            ["zzz", "aab", 1],
            ["xxx", "ddd", 2],
            ["xxx", "dde", 1],
            ["yyy", "fff", 1]
        ]

        result = find_correct_names(names)

        self.assertTrue(
            (
                result["correct_firstname"] ==
                Series(["aaa", "aaa", "ddd", "ddd", "fff"])
            ).all()
        )
        self.assertTrue(
            (
                result["correct_lastname"] ==
                Series(["zzz", "zzz", "xxx", "xxx", "yyy"])
            ).all()
        )

    def test_real_names(self):
        names = [
            ["Abbot", "Jim", "2"],
            ["Abbott", "James", "1"],
            ["Abbott", "Jim", "25"],
            ["Abbott", "Connie", "1"],
            ["Hoffman", "Abby", "1"],
            ["Abernethy-Gillis", "Robyn", "1"],
            ["Ablonczy", "Diane", "110"],
            ["Ablonczy", "Dianne", "1"],
            ["Ablonsky", "Diane", "1"],
            ["Ablonczy", "Honourable Diane", "2"]
        ]

        result = find_correct_names(names)

        print(names)
        print(result)

        self.assertTrue(
            (
                result["correct_firstname"] ==
                Series([
                    "Jim",
                    "Jim",
                    "Jim",
                    "Connie",
                    "Abby",
                    "Robyn",
                    "Diane",
                    "Diane",
                    "Diane",
                    "Diane"
                ])
            ).all()
        )
        self.assertTrue(
            (
                result["correct_lastname"] ==
                Series([
                    "Abbott",
                    "Abbott",
                    "Abbott",
                    "Abbott",
                    "Hoffman",
                    "Abernethy-Gillis",
                    "Ablonczy",
                    "Ablonczy",
                    "Ablonczy",
                    "Ablonczy"
                ])
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

