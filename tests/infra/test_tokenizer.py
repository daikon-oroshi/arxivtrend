import unittest
from arxivtrend.infra.tokenizer import Tokenizer


class TestWordExtract(unittest.TestCase):
    def setUp(self):
        self.extractor = Tokenizer()

    def test_remoove_linefeed_1(self):
        value = "aaa\nbbb"
        expected = "aaa bbb"
        actual = self.extractor._remove_linefeed(value)

        self.assertEqual(expected, actual)

    def test_remoove_tex_1(self):
        value = "aaa $\mathrm{R}$ bbb"
        expected = "aaa  bbb"
        actual = self.extractor._remove_tex(value)

        self.assertEqual(expected, actual)

    def test_remoove_tex_2(self):
        value = "aaa $\mathrm{R}$ bbb $\mathrm{N}$ ccc"
        expected = "aaa  bbb  ccc"
        actual = self.extractor._remove_tex(value)

        self.assertEqual(expected, actual)

    def test_remoove_tex_3(self):
        value = "aaa $$\mathrm{R}$$ bbb $\mathrm{C}$ ccc"
        expected = "aaa  bbb  ccc"
        actual = self.extractor._remove_tex(value)

        self.assertEqual(expected, actual)

    def test_tokenize(self):
        value = "The  library was   quiet, except for the soft rustle."
        expected = [
            "The", "library", "was", "quiet",
            ",", "except", "for", "the",
            "soft", "rustle", "."
        ]
        actual = self.extractor.tokenize(value)
        self.assertEqual(expected, actual)

    def test_remove_stopwords(self):
        """
        value = [
            TaggedToken(token='The', pos='DT'),  # 消える
            TaggedToken(token='library', pos='NN'),
            TaggedToken(token='was', pos='VBD'),  # 消える
            TaggedToken(token='quiet', pos='JJ'),
            TaggedToken(token=',', pos=','),  # 消える
            TaggedToken(token='except', pos='IN'),
            TaggedToken(token='for', pos='IN'),  # 消える
            TaggedToken(token='the', pos='DT'),  # 消える
            TaggedToken(token='soft', pos='JJ'),
            TaggedToken(token='rustle', pos='NN'),
            TaggedToken(token='.', pos='.')  # 消える
        ]
        expected = [
            TaggedToken(token='library', pos='NN'),
            TaggedToken(token='quiet', pos='JJ'),
            TaggedToken(token='except', pos='IN'),
            TaggedToken(token='soft', pos='JJ'),
            TaggedToken(token='rustle', pos='NN'),
        ]
        actual = self.extractor.remove_stopwords(value)
        self.assertEqual(expected, actual)
        """

    def test_filterby_pos_1(self):
        """
        value = [
            TaggedToken(token='She', pos='PRP'),
            TaggedToken(token='walked', pos='VBD'),
            TaggedToken(token='her', pos='PRP'),
            TaggedToken(token='dog', pos='NN'),
            TaggedToken(token='every', pos='DT'),
            TaggedToken(token='morning', pos='NN'),
            TaggedToken(token='rain', pos='NN'),
            TaggedToken(token='or', pos='CC'),
            TaggedToken(token='shine', pos='NN'),
            TaggedToken(token='enjoying', pos='VBG'),
            TaggedToken(token='peace', pos='NN'),
            TaggedToken(token='early', pos='JJ'),
            TaggedToken(token='hours', pos='NNS')
        ]
        expected = [
            TaggedToken(token='walked', pos='VBD'),
            TaggedToken(token='dog', pos='NN'),
            TaggedToken(token='morning', pos='NN'),
            TaggedToken(token='rain', pos='NN'),
            TaggedToken(token='shine', pos='NN'),
            TaggedToken(token='enjoying', pos='VBG'),
            TaggedToken(token='peace', pos='NN'),
            TaggedToken(token='early', pos='JJ'),
            TaggedToken(token='hours', pos='NNS')
        ]
        actual = self.extractor.filterby_pos(value)
        self.assertEqual(expected, actual)
        """

    def test_filterby_pos_2(self):
        """
        value = [
            TaggedToken(token="a", pos="FW"),
            TaggedToken(token="a", pos="JJ"),
            TaggedToken(token="a", pos="JJR"),
            TaggedToken(token="a", pos="JJS"),
            TaggedToken(token="a", pos="NN"),
            TaggedToken(token="a", pos="NNS"),
            TaggedToken(token="a", pos="NNP"),
            TaggedToken(token="a", pos="NNPS"),
            TaggedToken(token="a", pos="VB"),
            TaggedToken(token="a", pos="VBD"),
            TaggedToken(token="a", pos="VBG"),
            TaggedToken(token="a", pos="VBN"),
            TaggedToken(token="a", pos="VBP"),
            TaggedToken(token="a", pos="VBZ")
        ]
        expected = [
            TaggedToken(token="a", pos="FW"),
            TaggedToken(token="a", pos="JJ"),
            TaggedToken(token="a", pos="JJR"),
            TaggedToken(token="a", pos="JJS"),
            TaggedToken(token="a", pos="NN"),
            TaggedToken(token="a", pos="NNS"),
            TaggedToken(token="a", pos="NNP"),
            TaggedToken(token="a", pos="NNPS"),
            TaggedToken(token="a", pos="VB"),
            TaggedToken(token="a", pos="VBD"),
            TaggedToken(token="a", pos="VBG"),
            TaggedToken(token="a", pos="VBN"),
            TaggedToken(token="a", pos="VBP"),
            TaggedToken(token="a", pos="VBZ")
        ]
        actual = self.extractor.filterby_pos(value)
        self.assertEqual(expected, actual)
        """

    def test_lemmatize(self):
        ing_value = ('enjoying', 'VBG')
        ing_expected = "enjoy"
        ing_actual = self.extractor._lemmatize(*ing_value)
        self.assertEqual(ing_expected, ing_actual)

        ed_value = ('walked', 'VBD')
        ed_expected = "walk"
        ed_actual = self.extractor._lemmatize(*ed_value)
        self.assertEqual(ed_expected, ed_actual)

        s_value = ('hours', 'NNS')
        s_expected = "hour"
        s_actual = self.extractor._lemmatize(*s_value)
        self.assertEqual(s_expected, s_actual)


if __name__ == "__main__":
    unittest.main()
