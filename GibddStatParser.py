#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
from datetime import datetime
import codecs

def getLatestDate():
    year = datetime.now().year
    if datetime.now().month > 2:
        last_month = datetime.now().month - 1
    else:  # январь. придется брать данные за декабрь предыдущего года
        year -= 1
        last_month = 12
    return {"month":last_month, "year":year}

#1) получаем статистику ДТП по всей России. в ней - ОКАТО-коды всех регионов РФ (877 - код РФ)
#по умолчанию берем самые свежие данные, за месяц перед текущим (ГИБДД выгружает данные с отставанием на 1 месяц)
#возвращаем request.content
def getRusFedData():
    latest_m_y = getLatestDate()
    rf_dict = {"maptype":1,"region":"877","date":"[\"MONTHS:{0}.{1}\"]".format(latest_m_y["month"], latest_m_y["year"]),"pok":"1"}
    r = requests.post("http://stat.gibdd.ru/map/getMainMapData", json=rf_dict)
    if (r.status_code != 200):
        print(u"Не удалось получить данные по регионам РФ")
        return None
    else:
        print(u"Получены данные по регионам РФ")
        return r.content

#2) получаем пары код ОКАТО + название региона
def getRegionsInfo():
    content = getRusFedData()
    if content == None:
        return None
    else:
        regions = []
        d = (json.loads(content))
        regions_dict = json.loads(json.loads(d["metabase"])[0]["maps"])
        for rd in regions_dict:
            regions.append({"id": rd["id"], "name": rd["name"]})
        return regions

#3) получаем региональную статистику ДТП. в ней - ОКАТО-коды муниципальных образований для всех регионов
#по умолчанию берем самые свежие данные, за месяц перед текущим
#возвращаем request.content
def getRegionData(region_id, region_name):
    latest_m_y = getLatestDate()
    region_dict = {"maptype": 1, "date": "[\"MONTHS:{0}.{1}\"]".format(latest_m_y["month"], latest_m_y["year"]), "pok": "1"}
    region_dict["region"] = region_id  # region_id: string
    r = requests.post("http://stat.gibdd.ru/map/getMainMapData", json=region_dict)
    if (r.status_code != 200):
        print(u"Не удалось получить статистику по региону {0} {1}".format(region_id, region_name))
        return None
    else:
        print(u"Получена статистика по региону {0} {1}".format(region_id, region_name))
        return r.content

#4) получаем пары код ОКАТО + название муниципального образования для всех регионов
def getDistrictsInfo(region_id, region_name):
    content = getRegionData(region_id, region_name)
    if content == None:
        return None
    else:
        d = (json.loads(content))
        district_dict = json.loads(json.loads(d["metabase"])[0]["maps"])
        districts = []
        for dd in district_dict:
            districts.append({"id": dd["id"], "name": dd["name"]})
        return json.dumps(districts).encode('utf8').decode('unicode-escape')

#5) сохраняем справочник ОКАТО-кодов и названий регионов и муниципалитетов
def saveCodeDictionary(filename):
    region_codes = getRegionsInfo()
    for region in region_codes:
        region["districts"] = getDistrictsInfo(region["id"], region["name"])

    with codecs.open(filename, "w", encoding="utf-8") as f:
        json.dump(region_codes, f, ensure_ascii=False)


#6) карточки ДТП по заданному региону и муниципалитету за заданное время
#возвращаем request.content
def getDTPData(region_id, region_name, district_id, district_name, months, year):
    cards_dict = {"data": {"date":["MONTHS:1.2017"],"ParReg":"71100","order":{"type":"1","fieldName":"dat"},"reg":"71118","ind":"1","st":"1","en":"16"}}
    cards_dict["data"]["ParReg"] = region_id
    cards_dict["data"]["reg"] = district_id
    months_list = []
    for month in months:
        months_list.append("MONTHS:" + str(month) + "." + str(year))
    cards_dict["data"]["date"] = months_list
    # генерируем компактную запись json, без пробелов. иначе сайт не воспринимает данные
    cards_dict["data"] = json.dumps(cards_dict["data"], separators=(',', ':')).encode('utf8').decode(
            'unicode-escape')
    r = requests.post("http://stat.gibdd.ru/map/getDTPCardData", json=cards_dict)
    if (r.status_code != 200):
        print(u"Не удалось получить данные для {0} ({1}) за {2}-{3}.{4}".
              format(region_name, district_name, months[0], months[len(months) - 1], year))
        return None
    return r.content

#6) получаем детальную статистику ДТП по всем регионам РФ. один файл = один год
#возвращаем словарь со всеми карточками
#region_id='0' - получить данные по всем регионам. иначе - ОКАТО-номер региона
def getDTPInfo(year, months, regions, region_id="0"):
    dtp_cards = []

    for region in regions:
        # была запрошена статистика по одному из регионов, а не по РФ
        if region_id != "0" and region["id"] != region_id:
            continue

        districts = json.loads(region["districts"])
        for district in districts:
            content = getDTPData(region["id"], region["name"], district["id"], district["name"], months, year)
            if content == None:
                continue

            #получение карточек ДТП
            print(u"Обрабатываются данные для {0} ({1}) за {2}-{3}.{4}".
                  format(region["name"], district["name"], months[0], months[len(months)-1], year))
            cards_dict = (json.loads(content))
            cards = json.loads(cards_dict["data"])["tab"]
            for card in cards:
                card.pop('rowNum', None)
                card["Region"] = region["name"]

            dtp_cards.append(cards)

    #записываем json для года
    dtp_dict = {"data": {"year":str(year)}}
    dtp_dict["data"]["cards"] = dtp_cards
    dtp_dict_json = dtp_dict.copy()
    dtp_dict_json["data"] = json.dumps(dtp_dict_json["data"]).encode('utf8').decode('unicode-escape')

    return dtp_dict_json


import sys
import argparse

def createParser():
    parser = argparse.ArgumentParser(description="GibddStatParser.py [--year] [--months] [--regcode] [--outfilename] [--updatecodes] [--help]")
    parser.add_argument('--year', default=str(datetime.now().year), type=str,
        help = u'год, за который выводится статистика. примеры: --year 2017, --year 2015-2017')
    parser.add_argument('--month', default="1", type=str,
        help = u'временной период (в месяцах). примеры: --months 1, --months 1-12')
    parser.add_argument('--regcode', default='0', type=str,
        help = u'ОКАТО-код региона (см. в regions.json). пример для Москвы: --regcode 45')
    parser.add_argument('--outfilename', type=str,
        help = u'имя файла для сохранения карточек ДТП')
    parser.add_argument('--updatecodes', default='y', help = u'обновить справочник регионов. пример: --updatecodes y')
    return parser

def getParamSplitted(param, command_name):
    splitted_list = []
    splitted = param.split("-")
    try:
        splitted_list.append(int(splitted[0]))
        if len(splitted) == 2:
            splitted_list.append(int(splitted[1]))
    except:
        print(u"Неверное значение параметра {}".format(command_name))
    return splitted_list


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    if len(namespace.updatecodes) > 0:
        if namespace.updatecodes == "y":
            print (u"Обновление справочника кодов регионов...")
            saveCodeDictionary("regions.json")
            print(u"Обновление справочника завершено")
        else:
            print(u"Неверное значение параметра --updatecodes")
        return

    #получаем диапазон по годам
    years = getParamSplitted(namespace.year, "--year")

    #получаем диапазон по месяцам
    if namespace.month != None:
        months = getParamSplitted(namespace.month, "--month")
    else:
        if years[len(years)-1] == datetime.now().year:
            months = [1, datetime.now().month-1]
        else:
            months = [1, 12]

    #Тест: читаем данные из существующего справочника ОКАТО-кодов регионов и муниципалитетов
    filename = "regions.json"
    with codecs.open(filename, "r", "utf-8") as f:
        regions = json.loads(json.loads(json.dumps(f.read())))

    if len(years) == 1:
        years_list = years
    else:
        years_list = [i for i in range(years[0], years[1]+1)]
    if len(months) == 1:
        months_list = months
    else:
        months_list = [i for i in range(months[0], months[1]+1)]

    for year in years_list:
        card_dict = getDTPInfo(year, months_list, regions, region_id=namespace.regcode)
        if card_dict:
            #сохраняем данные карточек ДТП для выбранного года в файл
            with codecs.open(namespace.outfilename, "w", encoding="utf-8") as f:
                json.dump(card_dict, f, ensure_ascii=False, separators=(',', ':'))
                print(u"Сохранены данные для {0} года в {1}".format(year, namespace.outfilename))

    # Тест: читаем сохраненные данные ДТП
    # with codecs.open("dtp_cards_" + str(year) + ".json", "r", encoding="utf-8") as f:
    #     json_content = json.loads(json.dumps(f.read()))
    #     print (json_content)

#для вызова скрипта из командной строки
if __name__ == '__main__':
    print (u"Загрузчик данных по ДТП ГИБДД РФ")
    main()
