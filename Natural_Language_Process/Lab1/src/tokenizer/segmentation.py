from copy import deepcopy
from typing import List
from utils.vocabulary import Vocabulary
from utils.phrase import Phrase
from tqdm import tqdm


class OmniSegmentation(object):
    def __init__(self, vocabulary: Vocabulary):
        self.__vocabulary = deepcopy(vocabulary)

    def __call__(self, lines: List[List[str]]) -> List[List[str]]:
        ret: List[List[str]] = []
        for line in tqdm(lines):
            ret.append(self.__segmentation(line[0]))
        return ret

    def __segmentation(self, line: str) -> List[str]:
        EPS = 1e-8

        length = len(line)
        graph = Graph(length + 1)

        for i in range(length):
            for j in range(i, length):
                if i == j:
                    graph.add(i, j + 1, Phrase([line[i:j + 1]], 1))
                    continue

                phrase = self.__vocabulary.get(line[i:j + 1])
                if phrase is not None:
                    graph.add(i, j + 1, phrase)

        f: List[Edge] = []
        v: List[float] = []
        c: List[int] = []

        from math import log
        from math import fabs

        f.append(Edge(-1, None))
        v.append(0)
        c.append(0)
        for i in range(1, length + 1):
            f.append(Edge(-1, None))
            v.append(float('-inf'))
            c.append(0)

            for e in graph.get(i):
                if fabs(v[i] - (v[e.target()] + log(e.phrase().occ()))
                        ) < EPS and c[i] > c[e.target()] + e.phrase().length():
                    c[i] = c[e.target()] + e.phrase().length()
                    f[i] = e
                elif v[i] < v[e.target()] + log(e.phrase().occ()):
                    v[i] = v[e.target()] + log(e.phrase().occ())
                    c[i] = c[e.target()] + e.phrase().length()
                    f[i] = e

        ret = []
        i = length
        while i != 0:
            ret = ret + f[i].phrase().words()[-1::-1]
            i = f[i].target()

        return reversed(ret)


class Graph(object):
    def __init__(self, size: int):
        """
        ???????????????

        :param size: ??????
        """
        self.__size = size
        self.__list = []
        for i in range(size):
            self.__list.append([])

    def add(self, start: int, end: int, phrase: Phrase):
        """
        ????????????end???start??????????????????phrase

        :param start: ????????????
        :param end: ????????????
        :param phrase: ????????????????????????
        """
        self.__list[end].append(Edge(start, phrase))

    def get(self, node: int):
        """
        ????????????????????????

        :param node: ???????????????
        """
        return deepcopy(self.__list[node])


class Edge(object):
    def __init__(self, target: int, phrase: Phrase):
        """
        ????????????

        :param target: ??????????????????
        :param phrase: ????????????
        """
        self.__target = target
        self.__phrase = deepcopy(phrase)

    def target(self):
        return self.__target

    def phrase(self):
        return deepcopy(self.__phrase)
