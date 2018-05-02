# -*- coding: UTF-8 -*-
import json
import codecs
import sys
import argparse
import os

def createParser():
    parser = argparse.ArgumentParser(description="read_dtp_data.py [--filename]")
    parser.add_argument('--filename', type=str,
        help = u'имя файла данных. пример: --filename "45 г. Москва 1-12.2017.json"')
    return parser

def getParamSplitted(param, command_name):
    splitted_list = []
    splitted = param.split("-")
    try:
        splitted_list.append(int(splitted[0]))
        if len(splitted) == 2:
            splitted_list.append(int(splitted[1]))
    except:
        log_text = u"Неверное значение параметра {}".format(command_name)
        print(log_text)
    return splitted_list

def read_dtp_data(filename):
    with codecs.open(filename, "r", encoding="utf-8") as f:
        json_content = json.loads(json.loads(json.loads(json.dumps(f.read())))["data"])
        dtp_data = json_content["cards"]
        print("Статистика ДТП по {} за {}-{}.{}. Количество ДТП: {}".format(json_content["region_name"],
                json_content["month_first"], json_content["month_last"], json_content["year"], len(dtp_data)))
        print("Образец карточки ДТП: {}".format(dtp_data[0]))

def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if os.path.exists(namespace.filename):
        read_dtp_data(namespace.filename)

#для вызова скрипта из командной строки
if __name__ == '__main__':
    log_text = u"Проверка файла данных ДТП ГИБДД РФ"
    print(log_text)
    main()
