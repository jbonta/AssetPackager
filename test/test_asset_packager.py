import unittest

import AssetPackager

class SimpleTest(unittest.TestCase):

  def testAnalyze(self):
    def match(a, b):
      self.assertEqual(AssetPackager.analyze(a), b)

    match(
      [
        # 6 pages' worth of assets:
        ['/static/jquery.js', '/static/sitecore.js', '/foo/stuff/lost.js'],
        ['/static/jquery.js', '/static/sitecore.js', '/foo/stuff/found.js'],
        ['/static/errorPage.css', '/static/404.css'],
        ['/static/jquery.js', '/static/sitecore.js'],
        ['/static/jquery.js', '/static/sitecore.js'],
        ['/static/jquery.js', '/static/sitecore.js']
      ],
      [
        # output as 4 packages
        ['/static/jquery.js', '/static/sitecore.js'],
        ['/foo/stuff/lost.js'],
        ['/foo/stuff/found.js'],
        ['/static/errorPage.css', '/static/404.css'],
      ]
    )

    match(
      [
        list('abcd'),
      ],
      [
        list('abcd'),
      ]
    )

    match(
      [
        list('abcd'),
        list('abcd'),
        list('abcd'),
        list('vw'),
      ],
      [
        list('abcd'),
        list('vw'),
      ]
    )

    match(
      [
        list('abcdef'),
        list('abcd'),
        list('abcdg'),
      ],
      [
        list('abcd'),
        list('ef'),
        list('g'),
      ]
    )

    match(
      [
        list('adbc'),
        list('abcd'),
      ],
      [
        list('bc'),
        list('a'),
        list('d'),
      ]
    )

    match(
      [
        list('abcdkl'),
        list('abcdefghij'),
        list('abcdm'),
      ],
      [
        list('abcd'),
        list('kl'),
        list('efghij'),
        list('m'),
      ]
    )
