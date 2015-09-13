from unittest import TestCase

from src.data.clean import clean_name


class TestCleanName(TestCase):

    def test_all_caps(self):
        name = "TESTNAME"
        expected = "Testname"
        result = clean_name(name)
        self.assertEqual(result, expected)

    def test_leading_whitespace(self):
        name = " Test"
        expected = "Test"
        result = clean_name(name)
        self.assertEqual(result, expected)

    def test_trailing_whitespace(self):
        name = "Test "
        expected = "Test"
        result = clean_name(name)
        self.assertEqual(result, expected)

    def test_punctuation(self):
        name = ".Test"
        expected = "Test"
        result = clean_name(name)
        self.assertEqual(result, expected)

    def test_title(self):
        name = "Honourable Test"
        expected = "Test"
        result = clean_name(name)
        self.assertEqual(result, expected)

    def test_embedded_title(self):
        name = "Honourabletest"
        expected = "Honourabletest"
        result = clean_name(name)
        self.assertEqual(result, expected)

    def test_title_with_punctuation(self):
        name = "The Right Hon. Test"
        expected = "Test"
        result = clean_name(name)
        self.assertEqual(result, expected)

