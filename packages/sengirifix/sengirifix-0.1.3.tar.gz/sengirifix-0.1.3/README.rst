sengiri
==========
|travis| |coveralls| |pyversion| |version| |license|

Yet another sentence-level tokenizer for the Japanese text

DEPENDENCIES
==============

- MeCab
- emoji

INSTALLATION
==============

::

 $ pip install sengiri


USAGE
============

.. code:: python

  import sengiri

  print(sengiri.tokenize('うーん🤔🤔🤔どうしよう'))
  #=>['うーん🤔🤔🤔', 'どうしよう']
  print(sengiri.tokenize('モー娘。のコンサートに行った。'))
  #=>['モー娘。のコンサートに行った。']
  print(sengiri.tokenize('ありがとう＾＾ 助かります。'))
  #=>['ありがとう＾＾', '助かります。']
  print(sengiri.tokenize('顔文字テスト(*´ω｀*)うまくいくかな？'))
  #=>['顔文字テスト(*´ω｀*)うまくいくかな？']
  # I recommend using the NEologd dictionary.
  print(sengiri.tokenize('顔文字テスト(*´ω｀*)うまくいくかな？', mecab_args='-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'))
  #=>['顔文字テスト(*´ω｀*)', 'うまくいくかな？']
  print(sengiri.tokenize('子供が大変なことになった。'
                         '（後で聞いたのだが、脅されたらしい）'
                         '（脅迫はやめてほしいと言っているのに）'))
  #=>['子供が大変なことになった。', '（後で聞いたのだが、脅されたらしい）', '（脅迫はやめてほしいと言っているのに）']
  print(sengiri.tokenize('楽しかったw また遊ぼwww'))
  #=>['楽しかったw', 'また遊ぼwww']
  print(sengiri.tokenize('http://www.inpaku.go.jp/'))
  #=>['http://www.inpaku.go.jp/']

.. |travis| image:: https://travis-ci.org/ikegami-yukino/sengiri.svg?branch=master
    :target: https://travis-ci.org/ikegami-yukino/sengiri
    :alt: travis-ci.org

.. |coveralls| image:: https://coveralls.io/repos/ikegami-yukino/sengiri/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/ikegami-yukino/sengiri?branch=master
    :alt: coveralls.io

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/sengiri.svg

.. |version| image:: https://img.shields.io/pypi/v/sengiri.svg
    :target: http://pypi.python.org/pypi/sengiri/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/sengiri.svg
    :target: http://pypi.python.org/pypi/sengiri/
    :alt: license
