from django.test import TestCase
from design.recommend import getMarkovRecommend, get_chain, predict

class RecommendTestCase(TestCase):
    def setUp(self):
        self.partId = 1
    def test_MarkovRecommend(self):
        self.result = getMarkovRecommend(self.partId)
        self.isGet = self.result['isSuccessful']
        self.assertEqual(self.isGet, False)

class MarkovTestCase(TestCase):
    def test_get_chain(self):
        process = [{'f': [1, None]},
                   {'a': [0.5, 'f'], 'k': [0.5, 'f']},
                   {'j': [0.5, 'k'], 'g': [0.5, 'a']}]
        ans = ['f', 'k', 'j']
        res = get_chain('j', 2, process)
        self.assertEqual(ans, res, None)

    def test_predict(self):
        A = {'a': {'g': 1.0, 'j': 1.0},
             'g': {'f': 1.0},
             'f': {'a': 0.5, 'k': 0.5},
             'k': {'j': 0.5},
             'j': {'f': 1.0},
             'r': {'u': 1.0},
             'u': {'v': 1.0}}
        ss = ('f', 'b')
        anss = ([['a', 'j'], ['a', 'g']], None)
        for s, ans in zip(ss, anss):
            res = predict(2, 2, s, A)
            self.assertEqual(res, ans, None)