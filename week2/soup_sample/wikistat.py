from bs4 import BeautifulSoup
import re
import os
import json

# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}

    # files = os.listdir(path)
    for key in files.keys():
        # print(key)
        file_name = path + key
        p = []
        with open(file_name, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            soup = soup.find('div', id='bodyContent')
        all_a = soup.find_all('a', href=True)
        for a in all_a:
            res = re.sub('/wiki/', '', a['href'])
            if res in files.keys() and res not in p:
                p.append(res)
        files[key] = p
    # with open('info.txt', 'w') as f:
    #     f.write(json.dumps(files))
    return files

# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    a = build_tree(start, end, path)
    # info = ''
    # with open('info.txt', 'r') as f:
    #     for line in f:
    #         info += line
    #     a = json.loads(info)

    keys = list(a.keys())
    n = len(keys)
    matrix_s = []
    for key in keys:
        p = [0 for x in range(n)]
        for line in a[key]:
            p[keys.index(line)] = 1
        matrix_s.append(p)

    start_i = keys.index(start)
    end_i = keys.index(end)
    d = [float('inf') for i in range(n)]
    v = [1 for i in range(n)]

    d[start_i] = 0
    minindex = 0
    prev = [-1 for i in range(n)]

    while minindex < float('inf'):
        minindex = float('inf')
        min = float('inf')
        for i in range(n):
            if v[i] == 1 and d[i] < min:
                min = d[i]
                minindex = i

        if minindex != float('inf'):
            for i in range(n):
                if matrix_s[minindex][i] > 0:
                    temp = min + matrix_s[minindex][i]
                    if temp <= d[i]:
                        d[i] = temp
                        prev[i] = minindex

            v[minindex] = 0

    j = end_i
    mas = []
    # mas.append(j)
    while j != -1:
        mas.append(keys[j])
        j = prev[j]
    return mas[::-1]

    # print(files['Computer_architecture']['Virtual_machine'])

def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        imgs = 0
        # TODO посчитать реальные значения
        for img in body.find_all('img'):
            if 'width' in img.attrs:
                if int(img['width']) >= 200:
                    imgs += 1
        # imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        headers = 0
        for i in range(6):
            for header in body.find_all('h'+str(i)):
                text = header.get_text()
                if re.search('^\s?[ETC]', text):
                    headers += 1
        mas = []
        max = 0
        for link in body.find_all('a'):
            q = 1
            while link.find_next_sibling() != None:
                prev = link.find_next_sibling()
                if prev.name == 'a':
                    q += 1
                    link = prev
                else:
                    break

            if max < q:
                max = q
        linkslen = max
        lists = 0
        mas = ['ul', 'ol']
        for m in mas:
            for link in body.find_all(m):
                prevs = link.find_parents()
                p = False
                i = 0
                while not p and i < len(prevs):
                    if prevs[i].name in ['li', 'ol', 'ul']:
                        p = True
                    else:
                        i += 1
                if p == False:
                    lists += 1

        out[file] = [imgs, headers, linkslen, lists]

        # break

    return out

# print(parse('Stone_Age', 'Python_(programming_language)', 'wiki/'))
