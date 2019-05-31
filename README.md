# Парсер статистики ДТП с официального сайта ГИБДД stat.gibdd.ru

*Инструмент для исследователей, который позволяет скачивать актуальные подробные данные о ДТП с официального [сайта](http://stat.gibdd.ru/) статистики ДТП ГИБДД.* Подробности - в [статье](https://habr.com/post/354782/) на хабре.

![](https://github.com/Shorstko/GibddStat/blob/master/image/title.png)

Парсер работает из командной строки. Данные загружаются в формате `json`, в разбивке `один файл = один регион`. Папка с данными (по умолчанию `dtpdata`) создается рядом со скриптом. 

Парсер поддерживает докачку (т.к. не всегда удается скачать такой объем данных с первого раза), поэтому при повторном запуске пропускает уже скачанные регионы. 

Парсер пишет лог-файл с названием `parselog.log` со всей статистикой. По умолчанию данные дописываются и не обрезаются. Если нужен "чистый" лог, необходимо удалить этот файл.

Для корректной работы парсера в той же папке должен лежать справочник ОКАТО-кодов регионов [regions.json](https://github.com/Shorstko/GibddStat/blob/master/regions.json). Если справочника по какой-то причине нет, можно просто запустить парсер с параметром `--updatecodes y`, и справочник будет создан заново.

Также всю статистику ДТП можно взять [здесь](https://github.com/Shorstko/GibddStat/releases). За подсказку спасибо [espdev](https://github.com/espdev).

## Запуск парсера

Работает из командной строки. Базовый синтаксис: 
>   GibddStatParser.py [--year] [--month] [--regcode] [--dir] [--updatecodes] [--help]

`--year` год, за который скачивается статистика. если год не указан, скачивается статистика за текущий год

`--month` месяц, за который скачивается статистика. если не указан, скачивается статистика за все прошедшие месяцы года

`--regcode` ОКАТО-код региона. номера кодов регионов можно посмотреть в справочнике кодов регионов [regions.json](https://github.com/Shorstko/GibddStat/blob/master/regions.json) (параметр `id`)

`--dir` папка, в которую скачивается статистика. по умолчанию `dtpdata`

`--updatecodes` обновить ОКАТО-коды регионов с сайта stat.gibdd.ru. по умолчанию обновление отключено (`--updatecodes n`). Для корректной работы парсера справочник регионов `regions.json` должен лежать рядом со скриптом

**Примеры вызова парсера**

`GibddStatParser.py --year 2018` : скачать все ДТП за 2018 год. для текущего года скачиваются все месяцы минус текущий. для прошедших лет скачиваются 12 месяцев

`GibddStatParser.py --year 2018 --month 4` : скачать все ДТП за апрель 2018 года

`GibddStatParser.py --year 2018 --regcode 45` : скачать все ДТП по Москве за 2018 год. 45 - ОКАТО-код г.Москва

`GibddStatParser.py --year 2018 --updatecodes y` : скачать все ДТП за 2018 год и обновить справочник кодов регионов

## Проверка результатов

Для этого служит скрипт *read_dtp_data.py*. Синтаксис скрипта:
>  	read_dtp_data.py [--filename]

`--filename` имя файла в формате .json, содержащего карточки ДТП по какому-либо региону. необходимо указывать полный путь к файлу

**Пример**

`read_dtp_data.py --filename "c:\45 г. Москва 1-4.2018.json"` : просмотреть статистику ДТП по г.Москва за январь-апрель 2018 года (результат на картинке)

![просмотреть статистику ДТП по г.Москве за январь-апрель 2018 года](https://github.com/Shorstko/GibddStat/blob/master/image/test.png)

## Вызов парсера из командной строки Windows

Для непрограммистов будет достаточно установить [Python 3.6.5](https://www.python.org/downloads/release/python-365/) и вызывать скрипт из командной строки Windows. Например:

>   c:\Python36\Scripts\python.exe c:\GibddStatParser.py --year 2018

## Технические параметры

Код парсера написан на Python 3.6.5.

Установите зависимости перед запуском скрипта:

>   pip install -r requirements.txt

## Описание полей
### Общие поля структуры `data`
`year` - Год за который была совершена выгрузка
`region_code` - Код региона
`region_name` - Название региона

### Поля структуры `Card`
| `Название_поля_json` | `Человеческое_название_поля` | `тип данных`        | описание                            |
|:--------------------:|:----------------------------:|:-------------------:|:-----------------------------------:|
| `-`                  | `yeat`                       | string              | Год карточки                        |
| `-`                  | `region_code`                | string              | Код региона                         |
| `-`                  | `region_name`                | string              | Название региона                    |
| `KartId`             | `card_id`                    | int                 | ID карточки ДТП                     |
| `rowNum`             | `row_num`                    | int                 | не известно для чего нужно это поле |
| `date`               | `date`                       | string              | дата ДТП                            |
| `Time`               | `time`                       | string              | время ДТП                           |
| `District`           | `district`                   | string              | район ДТП                           |
| `DTP_V`              | `traffic_accident`           | string              | причина ДТП                         |
| `POG`                | `number_dead`                | int                 | число погибших                      |
| `RAN`                | `injured_number`             | int                 | число пострадавших                  |
| `K_TS`               | `vehicle_number`             | int                 | количество ТС                       |
| `K_UCH`              | `participants_number`        | int                 | количество участников               |
| `infoDtp`            | `traffic_accident_info`      | TrafficAccidentInfo | информация о ДТП                    |

### Поля структуры `TrafficAccidentInfo`

| `Название_поля_json` | `Человеческое_название_поля` |  `тип данных`  |                                 описание                                |
|:--------------------:|:----------------------------:|:--------------:|:-----------------------------------------------------------------------:|
|         `ndu`        | `road_network_disadvantages` |    []string    | недостатки транспортного и эксплуатационного обслуживания дорожной сети |
|        `sdor`        |        `RN_object_TA`        |    []string    |    объекты УДС на месте ДТП (RN - road network TA - traffic accident)   |
|       `ts_info`      |        `vehicle_info`        |  []VehicleInfo |                   информация о транспортных средствах                   |
|         `n_p`        |      `human_settlement`      |     string     |                             населенный пункт                            |
|       `street`       |           `street`           |     string     |                              название улицы                             |
|        `house`       |            `house`           |     string     |                                номер дома                               |
|         `dor`        |          `road_name`         |     string     |                             название дороги                             |
|         `km`         |             `km`             |     string     |                             номер километра                             |
|          `m`         |              `m`             |     string     |                               номер метра                               |
|        `k_ul`        |       `street_category`      |     string     |                             категория улицы                             |
|        `dor_k`       |        `road_category`       |     string     |                             категория дороги                            |
|        `dor_z`       |       `road_importance`      |     string     |                             значение дороги                             |
|       `factor`       |           `factor`           |    []string    |                               факторы ДТП                               |
|        `s_pog`       |      `weather_condition`     |    []string    |                             погодные условия                            |
|        `s_pch`       |    `carriageway_condition`   |     string     |                         состояние проезжей части                        |
|         `osv`        |          `lighting`          |     string     |          освещенность (например светлое или темное время суток)         |
|  `change_org_motion` |    `сhanges_movement_mode`   |     string     |                         режим изменения движения                        |
|        `s_dtp`       |  `TA_carriageway_condition`  |     string     |                  Состояние проезжей части во время ДТП                  |
|       `COORD_W`      |          `latitude`          | string, double |                                  Широта                                 |
|       `COORD_L`      |          `longitude`         | string, double |                                 Долгота                                 |
|       `OBJ_DTP`      |         `objects_TA`         |    []string    |                               объекты ДТП                               |
|       `uchInfo`      |      `participant_info`      |    []object    |                          информацие об участниках                       |

### Поля структуры `VehicleInfo`

| `Название_поля_json` | `Человеческое_название_поля` |     `тип данных`     |                                               описание                                               |
|:--------------------:|:----------------------------:|:--------------------:|:----------------------------------------------------------------------------------------------------:|
|        `n_ts`        |       `vehicle_number`       |      string, int     |                                               номер ТС                                               |
|        `ts_s`        |                              |        string        |                                       не удалось разобрать поле                                      |
|        `t_ts`        |            `type`            |        string        |                                                тип ТС                                                |
|      `marka_ts`      |            `brand`           |        string        |                                               марка ТС                                               |
|        `m_ts`        |            `model`           |        string        |                                               модель ТС                                              |
|        `color`       |            `color`           |        string        |                                                цвет ТС                                               |
|        `r_rul`       |      `transmission_type`     |        string        |                  тип трансмиссии (полноприводные, заднеприводные, переднеприводные)                  |
|         `g_v`        |      `manufacture_year`      |      string, int     |                                            год выпуска ТС                                            |
|        `m_pov`       |                              |        string        | Гугл говорит, что это значит https://ru.wikipedia.org/wiki/Википедия:Мегаломаниакальная_точка_зрения |
|         `t_n`        |      `technical_failure`     |        string        |                                       технические неисправности                                      |
|        `f_sob`       |       `ownership_form`       |        string        |                                          форма собственности                                         |
|        `o_pf`        |         `legal_form`         |        string        |                                     организационно-правовая форма                                    |
|       `ts_uch`       |     `vehicle_participant`    | []VehicleParticipant |                                             ТС учатсника                                             |

### Поля структуры `VehicleParticipant`

| `Название_поля_json` | `Человеческое_название_поля` | `тип данных` |                            описание                           |
|:--------------------:|:----------------------------:|:------------:|:-------------------------------------------------------------:|
|        `K_UCH`       |          `category`          |    string    |                      категория участника                      |
|        `NPDD`        |    `direct_violations_RoR`   |   []string   |         Прямые нарушения ПДД (RoR - Rules of the Road)        |
|         `S_T`        |          `severity`          |    string    |                        степень тяжести                        |
|         `POL`        |             `sex`            |    string    |                              пол                              |
|        `V_ST`        |     `driving_experience`     |  string, int |                         опыт вождения                         |
|        `ALCO`        |     `intoxication_degree`    |    string    |                 степень алкогольного опьянения                |
|      `SOP_NPDD`      |   `related_violations_RoR`   |   []string   |                  сопутствующие нарушения ПДД                  |
|     `SAFETY_BELT`    |       `use_safety_belt`      |    string    |               использовался ремень безопасности               |
|        `S_SM`        |          `leave_TA`          |    string    |                       покинул место ДТП?                      |
|        `N_UCH`       |     `number_participant`     |  string, int |                      номер участника ДТП                      |
|    `S_SEAT_GROUP`    |         `seat_group`         |    string    | группа сидения (скорей всего подразумевается десткое сиденье) |
|   `INJURED_CARD_ID`  |       `injured_card_id`      |    string    |                       неизвестно что это                      |
