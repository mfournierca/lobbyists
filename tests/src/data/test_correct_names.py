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
            ["xxx", "aaa", 2],
            ["xxx", "aab", 1],
            ["yyy", "ddd", 2],
            ["yyy", "dde", 1],
            ["zzz", "fff", 1]
        ]

        result = find_correct_names(names)

        self.assertTrue(
            (
                result["correct_firstname"] ==
                Series(["aaa", "aaa", "ddd", "ddd", "fff"])
            ).all(),
            "\n{0}".format(result)
        )
        self.assertTrue(
            (
                result["correct_lastname"] ==
                Series(["xxx", "xxx", "yyy", "yyy", "zzz"])
            ).all(),
            "\n{0}".format(result)
        )

    def test_real_names(self):
        names = [
            (u"Abbot", u"Jim", 2),
            (u"Abbott", u"James", 1),
            (u"Abbott", u"Jim", 25),
            (u"Abbott", u"Connie", 1),
            (u"Hoffman", u"Abby", 1),
            (u"Abernethy-Gillis", u"Robyn", 1),
            (u"Ablonczy", u"Diane", 110),
            (u"Ablonczy", u"Dianne", 1),
            (u"Ablonsky", u"Diane", 1),
            (u"Ablonczy", u"Honourable Diane", 2)
        ]

        expected = DataFrame()
        expected["correct_lastname"] = Series([
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
        expected["correct_firstname"] = Series([
            "Jim",
            "Jim",
            "Jim",
            "Connie",
            "Abby",
            "Robyn",
            "Diane",
            "Diane",
            "Diane",
            "Honourable Diane"
        ])

        result = find_correct_names(names)

        result = result.sort(["correct_lastname", "correct_firstname"])
        expected = expected.sort(["correct_lastname", "correct_firstname"])

        self.assertTrue(
            (
                result["correct_firstname"] == expected["correct_firstname"]
            ).all()
        )
        self.assertTrue(
            (
                result["correct_lastname"] == expected["correct_lastname"]
            ).all()
        )


class TestClusterAndLabel(TestCase):

    def runTest(self):
        pass

    def setUp(self):
        self.df = DataFrame(
            [
                ["xxx", "aaa", 2],
                ["xxx", "aab", 1],
                ["yyy", "ccc", 1],
                ["zzz", "ddd", 2],
                ["zzz", "dde", 1]
            ],
            columns=["lastname", "firstname", "count"]
        )
        self.df["name"] = self.df["lastname"] + self.df["firstname"]

    def tearDown(self):
        del self.df

    def test_cluster_labels(self):
        expected = [0, 0, 1, 2, 2]
        result = _cluster_and_label(self.df, column="name", label="label")
        result = result.sort(["name"])
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

