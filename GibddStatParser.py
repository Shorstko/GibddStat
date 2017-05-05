import requests
import json

#РФ, содержит все ОКАТО-коды регионов. maptype = 1 картограмма, region = ОКАТО-код РФ 877,
# date = период, за который запрашивается статистика, pok = 1 номер показателя (переписать с карты
html_data_initial = {"maptype":1,"region":"877","date":"[\"MONTHS:1.2017\"]","pok":"1"}
#ХМАО, ОКАТО региона 71140 получается из запроса по РФ. этим запросом получаем коды ОКАТО муниципалитетов
#в ответе id = ОКАТО, name = название района, города и т.п., path = номер трассы M651 и границы шейпа
html_data_initial = {"maptype":1,"region":"71100","date":"[\"MONTHS:1.2017\"]","pok":"1"}
#r = requests.post("http://stat.gibdd.ru/map/getMainMapData", json=html_data_initial)
#получение всех карточек ДТП по муниципалитету за выбранный период
#ParReg = region = ОКАТО-код региона, reg = ОКАТО-код муниципалитета
html_data_initial = {"data": {"date":["MONTHS:1.2017"],"ParReg":"71100","order":{"type":"1","fieldName":"dat"},"reg":"71118","ind":"1","st":"1","en":"16"}}
html_data_initial = {"data":"{\"date\":[\"MONTHS:1.2017\"],\"ParReg\":\"71100\",\"order\":{\"type\":\"1\",\"fieldName\":\"dat\"},\"reg\":\"71118\",\"ind\":\"1\",\"st\":\"1\",\"en\":\"16\"}"}

r = requests.post("http://stat.gibdd.ru/map/getDTPCardData", json=html_data_initial)
print (r.content)
rf_dict = json.loads(r.content)

'''
munc = dict()

metabase = json.loads(rf_dict["metabase"])
region_list = json.loads(metabase[0]["maps"])
print (r"\nДанные по региону raw: ", region_list[0])
print("Список муниципалитетов:")
for rl in region_list:
    for k, v in rl.items():
        print (k, ": ", v)

    munc[rl["id"]] = list({"info":""})

munc_data = json.loads(rf_dict["data"])
datasources = munc_data["MapChart"]["DataSources"]
print (r"\nПоказатели по муниципалитетам raw: ", datasources)
stat_list = datasources["DataSource"][0]["Dimension"]
for sl in stat_list:
    print (sl)
'''
dtp_data = json.loads(rf_dict["data"])["tab"]
print("\nКарточки ДТП:")
for dtp in dtp_data:
    print(dtp)

#print (r.json())
#print (json.loads(r.content))
#req = requests.Request('POST', "http://stat.gibdd.ru/map/getMainMapData", headers=html_headers_initial, json = html_data_initial)
#prepared = req.prepare()
#session = requests.Session()
#response = session.send(prepared)
