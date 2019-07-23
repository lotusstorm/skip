# -*- coding: utf-8 -*-
import re


PATH = 'dist/index.html'


def rewrite(text, results, iter_=0):
    """
    заменяет пути в тегах после сборки
    :param text: текст из файла
    :param results:
    :param iter_:
    :return:
    """

    if iter_ == 0:
        with open(PATH, 'w') as out:
            out.write(text)
        return

    if not isinstance(results, set):
        results = {results}

    result = results.pop()

    text = re.sub(result, '.{}'.format(result), text)
    rewrite(text, results, iter_=len(results))


def text_validator():
    """

    :return:
    """
    with open('dist/index.html', 'r') as inp:
        text = inp.read()
        pattern = re.compile(r'(href|src)=(/.*?\.(js|css))')
        results = [i[1] for i in re.findall(pattern, text)]

        rewrite(text, set(results), iter_=len(set(results)))


if __name__ == '__main__':
    text_validator()
