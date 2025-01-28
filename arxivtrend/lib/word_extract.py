from typing import List
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re
from pydantic import BaseModel


nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def get_wordnet_pos(treebank_tag: str) -> str:
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        # Default to noun if no match is found or starts with 'N'
        return wn.NOUN


class TaggedToken(BaseModel):
    token: str
    pos: str


class LemmatizedToken(TaggedToken):
    lemmatized: str


class WordExtractor():
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

    def preprocess(self, sentence):
        sentence = self._remove_linefeed(sentence)
        sentence = self._remove_citation(sentence)
        sentence = self._remove_tex(sentence)
        return sentence

    def remove_stopwords(
        self,
        tagged_tokens: List[TaggedToken]
    ) -> List[TaggedToken]:
        stop_words = nltk.corpus.stopwords.words('english') \
            + [".", ","]
        return [
            t for t in tagged_tokens
            if t.token.lower() not in stop_words
        ]

    def tokenize(self, sentence: str) -> List[str]:
        return nltk.tokenize.word_tokenize(sentence)

    def pos_tagging(self, tokens: List[str]) -> List[TaggedToken]:
        return [
            TaggedToken(token=token, pos=pos)
            for (token, pos) in nltk.pos_tag(tokens)
        ]

    def lemmatize(self, tagged_token: TaggedToken) -> str:
        return self.lemmatizer.lemmatize(
            tagged_token.token,
            pos=get_wordnet_pos(tagged_token.pos)
        )

    def filterby_pos(
        self,
        tagged_tokens: List[TaggedToken],
    ) -> List[TaggedToken]:
        return [
            t for t in tagged_tokens
            if t.pos in self.tag_fw
            + self.tag_adj
            + self.tag_noun
            + self.tag_verb
        ]

    def extract(self, sentence: str) -> List[str]:
        sentence = self.preprocess(sentence)
        tokens = self.tokenize(sentence)
        tagged_tokens = self.pos_tagging(tokens)
        tagged_tokens = self.remove_stopwords(tagged_tokens)
        tagged_tokens = self.filterby_pos(tagged_tokens)
        lemmatized_tokens = [
            LemmatizedToken(
                token=t.token,
                pos=t.pos,
                lemmatized=self.lemmatize(t)
            )
            for t in tagged_tokens
        ]
        return lemmatized_tokens
