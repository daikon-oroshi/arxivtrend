from typing import List
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re
from arxivtrend.domain.entities.token \
    import PosJpNotation, Token


class Tokenizer():

    @staticmethod
    def get_base_stopword() -> List[Token]:
        return nltk.corpus.stopwords.words('english') \
            + [".", ","]

    def __init__(self):
        self.tex_regex = re.compile(r'\$.+?\$')
        self.tex_regex_double = re.compile(r'\$\$.+?\$\$')
        self.cite_regex = re.compile(r'\[.*?\]')
        self.simbol_regex = re.compile(
            '[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」'
            '〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]'
            )
        self.lemmatizer = WordNetLemmatizer()

    tag_fw = [
        'FW'  # Foreign word 外国語
    ]
    tag_adj = [
        'JJ',  # Adjective 形容詞
        'JJR',  # Adjective, comparative 形容詞 (比較級)
        'JJS'  # Adjective, superlative 形容詞 (最上級)
    ]
    tag_noun = [
        'NN',  # Noun, singular or mass 名詞
        'NNS',  # Noun, plural 名詞 (複数形)
        'NNP',  # Proper noun, singular 固有名詞
        'NNPS'  # Proper noun, plural 固有名詞 (複数形)
    ]
    tag_verb = [
        'VB',  # Verb, base form 動詞 (原形)
        'VBD',  # Verb, past tense 動詞 (過去形)
        'VBG',  # Verb, gerund or present participle	動詞 (動名詞または現在分詞)
        'VBN',  # Verb, past participle	動詞 (過去分詞)
        'VBP',  # Verb, non-3rd person singular present	動詞 (三人称単数以外の現在形)
        'VBZ'  # Verb, 3rd person singular present	動詞 (三人称単数の現在形)
    ]

    def _get_wordnet_pos(self, treebank_tag: str) -> str:
        if treebank_tag.startswith('J'):
            return wn.ADJ
        elif treebank_tag.startswith('V'):
            return wn.VERB
        elif treebank_tag.startswith('R'):
            return wn.ADV
        else:
            # Default to noun if no match is found or starts with 'N'
            return wn.NOUN

    def _get_jp_pos(self, treebank_tag: str) -> PosJpNotation:
        if treebank_tag.startswith('J'):
            return PosJpNotation.ADJ
        elif treebank_tag.startswith('V'):
            return PosJpNotation.VERB
        elif treebank_tag.startswith('N'):
            return PosJpNotation.NOUN
        else:
            return PosJpNotation.OHTER

    def _remove_linefeed(self, sentence: str) -> str:
        return sentence.replace('\n', ' ')

    def _remove_citation(self, sentence: str) -> str:
        """
        引用文献を削除する。
        """
        return self.cite_regex.sub('', sentence)

    def _remove_tex(self, sentence: str) -> str:
        """
        texコマンドを削除。
        """
        _s = self.tex_regex_double.sub('', sentence)
        _s = self.tex_regex.sub('', _s)
        return _s

    def _preprocess(self, sentence):
        sentence = self._remove_linefeed(sentence)
        sentence = self._remove_citation(sentence)
        sentence = self._remove_tex(sentence)
        return sentence

    def _lemmatize(self, token: str, treebank_tag: str) -> str:
        return self.lemmatizer.lemmatize(
            token,
            pos=self._get_wordnet_pos(treebank_tag)
        )

    def tokenize(self, sentence: str) -> List[Token]:
        sentence = self._preprocess(sentence)
        tokens = nltk.tokenize.word_tokenize(sentence)
        tagged_tokens = nltk.pos_tag(tokens)
        lemmatized_tokens = [
            Token(
                word=self._lemmatize(t, treebank_tag),
                pos=self._get_jp_pos(treebank_tag)
            )
            for (t, treebank_tag) in tagged_tokens
        ]

        return lemmatized_tokens


if __name__ == "__main__":
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('averaged_perceptron_tagger_eng')