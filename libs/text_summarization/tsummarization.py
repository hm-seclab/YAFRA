'''

'''

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import pycountry

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from langdetect import detect

from libs.kafka.logging import LogMessage

def detect_lang(text, servicename):
    '''
    detect_lang will try to detect the language used by the report.
    @param text will be the text to check.
    @param servicename will be the name of the calling service. 
    @return the detected language as a string.
    '''
    try:
        lang = detect(text)
        country = pycountry.languages.get(alpha_2=str(lang))
        return str(country.name)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
        return "english"
    

def summarize(text, servicename):
    '''
    summarize will summarize the given text.
    @param text will be the text to summarize.
    @param servicename will be the name of the calling service. 
    @return the summarization as string.
    '''
    sum = ""
    try:
        SENTENCES_COUNT = 10
        lang = detect_lang(text, servicename).lower()
        parser = PlaintextParser.from_string(text, Tokenizer(lang))
        stemmer = Stemmer(lang)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(lang)
        sentences = summarizer(parser.document, SENTENCES_COUNT)
        for element in sentences: sum += str(element) + ". "
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return sum
