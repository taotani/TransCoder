import pytest
from .csharp_tokenize import tokenize_csharp, detokenize_csharp

TESTS = []
TESTS.append((
    r"""
// Hello World! program
namespace HelloWorld
{
    class Hello {         
        static void Main(string[] args)
        {
            System.Console.WriteLine("Hello World!");
        }
    }
}
    """,
    ['namespace', 'HelloWorld', 
    '{', 
    'class', 'Hello', '{', 
    'static', 'void', 'Main', '(', 'string', '[', ']', 'args', ')', 
    '{',
    'System', '.', 'Console', '.', 'WriteLine', '(', '" Hello SPACETOKEN World ! "', ')', ';', 
    '}', 
    '}',
    '}']
))

TESTS.append((r"""
overload((byte)1);
overload(1L);
overload(1.0f);""",
              ['overload', '(', '(', 'byte', ')', '1', ')', ';',
               'overload', '(', '1L', ')', ';',
               'overload', '(', '1.0f', ')', ';']
              ))

def test_csharp_tokenizer_discarding_comments():
    for i, (x, y) in enumerate(TESTS):
        y_ = tokenize_csharp(x)
        assert y_ == y

def test_csharp_detokenizer_discarding_comments():
    for i, x in enumerate([x[0] for x in TESTS]):
        tokens = tokenize_csharp(x)
        x_ = detokenize_csharp(tokens)
        tokens_ = tokenize_csharp(x_)
        assert tokens_ == tokens