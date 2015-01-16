import re
from nltk.corpus import wordnet


class RegexpReplacer(object):
    replacement_patterns = [
        (r"won\'t", 'will not'),
        (r"can\'t", 'cannot'),
        (r"i\'m", 'i am'),
        (r"ain\'t", 'is not'),
        (r"(\w+)\'ll", r'\1 will'),
        (r"(\w+)n\'t", '\g<1> not'),
        (r"(\w+)\'ve", '\g<1> have'),
        (r"(\w+)\'s", '\g<1> is'),
        (r"(\w+)\'re", '\g<1> are'),
        (r"(\w+)\'d", '\g<1> would')
    ]

    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for regex, repl in patterns]

    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            s = pattern.sub(repl, s)
        return s


def test_regex_replacer():
    replacer = RegexpReplacer()
    sents = ["can't is a contraction", "I'll go to Shanghai tomorrow"]
    for sent in sents:
        print sent
        print replacer.replace(sent)
    

class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        if wordnet.synsets(word):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word


def test_repeat_replacer():
    replacer = RepeatReplacer()
    sents = ['goose', 'looooove']
    for sent in sents:
        print sent
        print replacer.replace(sent)
    
            