from nose.tools import *
from ex49 import parser

def test_Sentence():
    parse = parser.Sentence(('noun', 'bear'), ('verb', 'go'), ('direction', 'north'))

    assert_equal(parse.subject, 'bear')
    assert_equal(parse.verb, 'go')
    assert_equal(parse.object, 'north')

def test_peek():
    assert_equal(parser.peek([('direction', 'north')]), 'direction')
    assert_equal(parser.peek([('verb', 'go'), ('direction', 'north')]), 'verb')
    assert_equal(parser.peek([('stop', 'of'), ('number', 1234), ('noun', 'princess')]), 'stop')
    assert_equal(parser.peek([]), None)

def test_match():
    assert_equal(parser.match([('direction', 'north')], 'direction'), ('direction', 'north'))
    assert_equal(parser.match([('direction', 'north')], 'verb'), None)
    assert_equal(parser.match([('verb', 'go'), ('direction', 'north')], 'verb'), ('verb', 'go'))
    assert_equal(parser.match([('stop', 'of'), ('number', 1234), ('noun', 'princess')], 'stop'), ('stop', 'of'))
    assert_equal(parser.match([('stop', 'of'), ('number', 1234), ('noun', 'princess')], 'verb'), None)

def test_parse_verb():
    assert_equal(parser.parse_verb([('stop', 'of'), ('verb', 'go'), ('direction', 'north')]), ('verb', 'go'))
    assert_equal(parser.parse_verb([('stop', 'the'), ('verb', 'go'), ('direction', 'north')]), ('verb', 'go'))
    assert_raises(parser.ParserError, parser.parse_verb, [('stop', 'in'), ('number', 1234), ('noun', 'princess')])

def test_parse_object():
    assert_equal(parser.parse_object([('noun', 'bear'), ('verb', 'go'), ('direction', 'north')]), ('noun', 'bear'))
    assert_equal(parser.parse_object([('direction', 'south'), ('verb', 'go'), ('noun', 'bear')]),
                 ('direction', 'south'))
    assert_raises(parser.ParserError, parser.parse_object, [('verb', 'kill'), ('stop', 'of'), ('verb', 'go')])

def test_parse_subject():
    sub1 = parser.parse_subject([('verb', 'go'), ('direction', 'north')], ('noun', 'princess'))
    assert_equal(sub1.subject, 'princess')
    assert_equal(sub1.verb, 'go')
    assert_equal(sub1.object, 'north')

    sub2 = parser.parse_subject([('verb', 'kill'), ('stop', 'of'), ('noun', 'bear')], ('noun', 'player'))
    assert_equal(sub2.subject, 'player')
    assert_equal(sub2.verb, 'kill')
    assert_equal(sub2.object, 'bear')

def test_parse_sentence():
    sen1 = parser.parse_sentence([('verb', 'kill'), ('stop', 'of'), ('noun', 'bear')])
    assert_equal(sen1.subject, 'player')
    assert_equal(sen1.verb, 'kill')
    assert_equal(sen1.object, 'bear')

    sen2 = parser.parse_sentence([('noun', 'princess'), ('stop', 'of'), ('verb', 'go'), ('direction', 'west')])
    assert_equal(sen2.subject, 'princess')
    assert_equal(sen2.verb, 'go')
    assert_equal(sen2.object, 'west')

    assert_raises(parser.ParserError, parser.parse_sentence,
                  [('stop', 'the'), ('stop', 'of'), ('direction', 'west'), ('verb', 'go')])