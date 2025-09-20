from sqlmodel import select

from app.core.config import admin_password, pwd_context
from app.core.enums import UserRole
from app.db.models import MedicalOrganisation, User
from app.db.session import async_session

mo_list = [
    MedicalOrganisation(mo_code=202, mo_name=r'ГБУЗ СО "БЕЗЕНЧУКСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=302, mo_name=r'ГБУЗ СО "БОГАТОВСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=402, mo_name=r'ГБУЗ СО "БОЛЬШЕГЛУШИЦКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=502, mo_name=r'ГБУЗ СО "БОЛЬШЕЧЕРНИГОВСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=602, mo_name=r'ГБУЗ СО "БОРСКАЯ ЦРБ"'),
    MedicalOrganisation(
        mo_code=701, mo_name=r'ГБУЗ СО "ВОЛЖСКАЯ РАЙОННАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА"'
    ),
    MedicalOrganisation(mo_code=802, mo_name=r'ГБУЗ СО "ИСАКЛИНСКАЯ ЦРБ"'),
    MedicalOrganisation(
        mo_code=902, mo_name=r'ГБУЗ СО "КИНЕЛЬСКАЯ ЦЕНТРАЛЬНАЯ РАЙОННАЯ БОЛЬНИЦА"'
    ),
    MedicalOrganisation(mo_code=1002, mo_name=r'ГБУЗ СО "КОШКИНСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=1102, mo_name=r'ГБУЗ СО "КРАСНОАРМЕЙСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=1202, mo_name=r'ГБУЗ СО "КРАСНОЯРСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=1302, mo_name=r'ГБУЗ СО "КИНЕЛЬ-ЧЕРКАССКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=1402, mo_name=r'ГБУЗ СО "КЛЯВЛИНСКАЯ ЦРБ"'),
    MedicalOrganisation(
        mo_code=1502, mo_name=r'ГБУЗ СО "НЕФТЕГОРСКАЯ ЦРБ ИМ. Н.И.ЗВЯГИНЦЕВА"'
    ),
    MedicalOrganisation(mo_code=1602, mo_name=r'ГБУЗ СО "ПЕСТРАВСКАЯ ЦРБ"'),
    MedicalOrganisation(
        mo_code=1702, mo_name=r'ГБУЗ СО "ПОХВИСТНЕВСКАЯ ЦЕНТРАЛЬНАЯ РАЙОННАЯ БОЛЬНИЦА"'
    ),
    MedicalOrganisation(mo_code=1802, mo_name=r'ГБУЗ СО "ПРИВОЛЖСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=1902, mo_name=r'ГБУЗ СО "СЕРГИЕВСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=2002, mo_name=r'ГБУЗ СО "СТАВРОПОЛЬСКАЯ ЦРБ"'),
    MedicalOrganisation(
        mo_code=2110, mo_name=r'ГБУЗ СО ПРОТИВОТУБЕРКУЛЕЗНЫЙ САНАТОРИЙ "РАЧЕЙКА"'
    ),
    MedicalOrganisation(mo_code=2202, mo_name=r'ГБУЗ СО "ЧЕЛНО-ВЕРШИНСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=2302, mo_name=r'ГБУЗ СО "ХВОРОСТЯНСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=2402, mo_name=r'ГБУЗ СО "ШЕНТАЛИНСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=2502, mo_name=r'ГБУЗ СО "ШИГОНСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=2602, mo_name=r'ГБУЗ СО "КАМЫШЛИНСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=2702, mo_name=r'ГБУЗ СО "ЕЛХОВСКАЯ ЦРБ"'),
    MedicalOrganisation(mo_code=3002, mo_name=r'ГБУЗ СО "ЖИГУЛЕВСКАЯ ЦГБ"'),
    MedicalOrganisation(mo_code=3102, mo_name=r'ГБУЗ СО "НОВОКУЙБЫШЕВСКАЯ ЦГБ"'),
    MedicalOrganisation(
        mo_code=3114,
        mo_name=r"ГБУЗ САМАРСКАЯ ОБЛАСТНАЯ СТАНЦИЯ СКОРОЙ МЕДИЦИНСКОЙ ПОМОЩИ",
    ),
    MedicalOrganisation(
        mo_code=3115, mo_name=r"ГБУЗ СО НОВОКУЙБЫШЕВСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА"
    ),
    MedicalOrganisation(
        mo_code=3202, mo_name=r'ГБУЗ СО "ОКТЯБРЬСКАЯ ЦЕНТРАЛЬНАЯ ГОРОДСКАЯ БОЛЬНИЦА"'
    ),
    MedicalOrganisation(
        mo_code=3302, mo_name=r'ГБУЗ СО "ОТРАДНЕНСКАЯ ГОРОДСКАЯ БОЛЬНИЦА"'
    ),
    MedicalOrganisation(mo_code=3409, mo_name=r'ГБУЗ СО "СЫЗРАНСКАЯ ЦГРБ"'),
    MedicalOrganisation(
        mo_code=3412, mo_name=r"ГБУЗ СО СЫЗРАНСКИЙ КОЖНО-ВЕНЕРОЛОГИЧЕСКИЙ ДИСПАНСЕР"
    ),
    MedicalOrganisation(
        mo_code=3413, mo_name=r"ГБУЗ СО СЫЗРАНСКИЙ НАРКОЛОГИЧЕСКИЙ ДИСПАНСЕР"
    ),
    MedicalOrganisation(
        mo_code=3414, mo_name=r"ГБУЗ СО СЫЗРАНСКИЙ ПСИХОНЕВРОЛОГИЧЕСКИЙ ДИСПАНСЕР"
    ),
    MedicalOrganisation(
        mo_code=3415, mo_name=r"ГБУЗ СО СЫЗРАНСКИЙ ПРОТИВОТУБЕРКУЛЕЗНЫЙ ДИСПАНСЕР"
    ),
    MedicalOrganisation(
        mo_code=3421, mo_name=r"ГБУЗ СО СЫЗРАНСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА"
    ),
    MedicalOrganisation(
        mo_code=3430, mo_name=r"ГКУЗ СО ДОМ РЕБЕНКА СПЕЦИАЛИЗИРОВАННЫЙ"
    ),
    MedicalOrganisation(
        mo_code=3501, mo_name=r'ГБУЗ СО "ЧАПАЕВСКАЯ ЦЕНТРАЛЬНАЯ ГОРОДСКАЯ БОЛЬНИЦА"'
    ),
    MedicalOrganisation(
        mo_code=3512, mo_name=r"ГАУЗ СО ЧАПАЕВСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА"
    ),
    MedicalOrganisation(
        mo_code=3519, mo_name=r"ООО КОНСУЛЬТАТИВНО-ДИАГНОСТИЧЕСКАЯ ПОЛИКЛИНИКА"
    ),
    MedicalOrganisation(
        mo_code=4003, mo_name=r"ГБУЗ СО ТОЛЬЯТТИНСКИЙ ПСИХОНЕВРОЛОГИЧЕСКИЙ ДИСПАНСЕР"
    ),
    MedicalOrganisation(
        mo_code=4004, mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКИЙ НАРКОЛОГИЧЕСКИЙ ДИСПАНСЕР"'
    ),
    MedicalOrganisation(
        mo_code=4005, mo_name=r"ГБУЗ СО ТОЛЬЯТТИНСКИЙ ПРОТИВОТУБЕРКУЛЕЗНЫЙ ДИСПАНСЕР"
    ),
    MedicalOrganisation(
        mo_code=4006, mo_name=r"ГБУЗ СО ТОЛЬЯТТИНСКАЯ СТАНЦИЯ СКОРОЙ МЕДИЦИНСКОЙ ПОМОЩИ"
    ),
    MedicalOrganisation(
        mo_code=4018,
        mo_name=r'ГБУ3 СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ ДЕТСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА"',
    ),
    MedicalOrganisation(mo_code=4019, mo_name=r'ПАО "КУЙБЫШЕВАЗОТ"'),
    MedicalOrganisation(mo_code=4020, mo_name=r"ООО МСЧ №6"),
    MedicalOrganisation(
        mo_code=4021,
        mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА № 2 ИМ.В.В.БАНЫКИНА"',
    ),
    MedicalOrganisation(
        mo_code=4022,
        mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА № 1 ИМ. В.А ГРОЙСМАНА"',
    ),
    MedicalOrganisation(
        mo_code=4023, mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ БОЛЬНИЦА № 4"'
    ),
    MedicalOrganisation(
        mo_code=4024,
        mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА № 5"',
    ),
    MedicalOrganisation(
        mo_code=4026, mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ ПОЛИКЛИНИКА № 1"'
    ),
    MedicalOrganisation(
        mo_code=4043,
        mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ ПОЛИКЛИНИКА № 3"',
    ),
    MedicalOrganisation(
        mo_code=4044,
        mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКИЙ ЛЕЧЕБНО-РЕАБИЛИТАЦИОННЫЙ ЦЕНТР "АРИАДНА"',
    ),
    MedicalOrganisation(
        mo_code=4048, mo_name=r"ГБУЗ СО ТОЛЬЯТТИНСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА № 1"
    ),
    MedicalOrganisation(
        mo_code=4049, mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКИЙ ДОМ РЕБЕНКА СПЕЦИАЛИЗИРОВАННЫЙ"'
    ),
    MedicalOrganisation(
        mo_code=4050, mo_name=r"ГБУЗ СО ТОЛЬЯТТИНСКИЙ КОЖНО-ВЕНЕРОЛОГИЧЕСКИЙ ДИСПАНСЕР"
    ),
    MedicalOrganisation(
        mo_code=4051,
        mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКИЙ ВРАЧЕБНО-ФИЗКУЛЬТУРНЫЙ ДИСПАНСЕР"',
    ),
    MedicalOrganisation(
        mo_code=4054, mo_name=r"ГБУЗ СО ТОЛЬЯТТИНСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА № 3"
    ),
    MedicalOrganisation(mo_code=4055, mo_name=r'МСЧ № 3 ОАО "ВОЛГОЦЕММАШ"'),
    MedicalOrganisation(
        mo_code=4057, mo_name=r"ФГБУ САНАТОРИЙ ЛЕСНОЕ МИНЗДРАВА РОССИИ"
    ),
    MedicalOrganisation(
        mo_code=4059, mo_name=r'ОАНО "ВУИТ" САНАТОРИЙ-ПРОФИЛАКТОРИЙ "РУССКИЙ БОР"'
    ),
    MedicalOrganisation(mo_code=4060, mo_name=r'ЗДРАВПУНКТ ООО "ТОЛЬЯТТИКАУЧУК"'),
    MedicalOrganisation(
        mo_code=4098, mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ ПОЛИКЛИНИКА № 2"'
    ),
    MedicalOrganisation(
        mo_code=4099, mo_name=r'ГБУЗ СО "ТОЛЬЯТТИНСКАЯ ГОРОДСКАЯ ПОЛИКЛИНИКА № 4"'
    ),
    MedicalOrganisation(
        mo_code=5002,
        mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА № 1 ИМ.Н.И.ПИРОГОВА"',
    ),
    MedicalOrganisation(
        mo_code=5003,
        mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА № 2 ИМ.Н.А.СЕМАШКО',
    ),
    MedicalOrganisation(mo_code=5008, mo_name=r"ГБУЗ  САМАРСКАЯ СМП"),
    MedicalOrganisation(
        mo_code=5009, mo_name=r"ООО ЦЕНТР КОСМЕТОЛОГИИ И ПЛАСТИЧЕСКОЙ ХИРУРГИИ"
    ),
    MedicalOrganisation(
        mo_code=5015,
        mo_name=r'ГБУЗ  "САМАРСКАЯ  ОБЛАСТНАЯ КЛИНИЧЕСКАЯ ГЕРИАТРИЧЕСКАЯ БОЛЬНИЦА"',
    ),
    MedicalOrganisation(
        mo_code=5017,
        mo_name=r'ГБУЗ "САМАРСКАЯ ОБЛАСТНАЯ ДЕТСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА ИМ.Н.Н.ИВАНОВОЙ"',
    ),
    MedicalOrganisation(
        mo_code=5018,
        mo_name=r'ГБУЗ "САМАРСКАЯ ОБЛАСТНАЯ ДЕТСКАЯ ИНФЕКЦИОННАЯ БОЛЬНИЦА"',
    ),
    MedicalOrganisation(
        mo_code=5025,
        mo_name=r"ГБУЗ СО САМАРСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА № 1",
    ),
    MedicalOrganisation(
        mo_code=5113,
        mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ ПОЛИКЛИНИКА № 13 ЖЕЛЕЗНОДОРОЖНОГО РАЙОНА"',
    ),
    MedicalOrganisation(
        mo_code=5201,
        mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ ПОЛИКЛИНИКА № 4 КИРОВСКОГО РАЙОНА"',
    ),
    MedicalOrganisation(
        mo_code=5202, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА № 8"'
    ),
    MedicalOrganisation(
        mo_code=5206, mo_name=r"ГБУЗ СО САМАРСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА № 6"
    ),
    MedicalOrganisation(
        mo_code=5207, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ БОЛЬНИЦА № 5"'
    ),
    MedicalOrganisation(
        mo_code=5306, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ БОЛЬНИЦА № 7"'
    ),
    MedicalOrganisation(
        mo_code=5401, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ БОЛЬНИЦА № 10"'
    ),
    MedicalOrganisation(
        mo_code=5403,
        mo_name=r"ГБУЗ СО САМАРСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА № 5 КУЙБЫШЕВСКОГО РАЙОНА",
    ),
    MedicalOrganisation(
        mo_code=5501, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ ПОЛИКЛИНИКА № 3"'
    ),
    MedicalOrganisation(
        mo_code=5602, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ БОЛЬНИЦА № 4"'
    ),
    MedicalOrganisation(
        mo_code=5606, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ ДЕТСКАЯ БОЛЬНИЦА № 2"'
    ),
    MedicalOrganisation(
        mo_code=5607, mo_name=r'МКУ ГО САМАРА ДОМ РЕБЕНКА "СОЛНЫШКО" СПЕЦИАЛИЗИРОВАННЫЙ'
    ),
    MedicalOrganisation(
        mo_code=5702,
        mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ КОНСУЛЬТАТИВНО-ДИАГНОСТИЧЕСКАЯ ПОЛИКЛИНИКА № 14"',
    ),
    MedicalOrganisation(mo_code=5705, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГП 2"'),
    MedicalOrganisation(
        mo_code=5708,
        mo_name=r"ГБУЗ СО САМАРСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА № 2 ПРОМЫШЛЕННОГО РАЙОНА",
    ),
    MedicalOrganisation(
        mo_code=5715,
        mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ КЛИНИЧЕСКАЯ ПОЛИКЛИНИКА № 15 ПРОМЫШЛЕННОГО РАЙОНА"',
    ),
    MedicalOrganisation(mo_code=5716, mo_name=r'ГБУЗ СО "СГП №6 ПРОМЫШЛЕННОГО РАЙОНА"'),
    MedicalOrganisation(
        mo_code=5721,
        mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ ПОЛИКЛИНИКА № 1 ПРОМЫШЛЕННОГО РАЙОНА"',
    ),
    MedicalOrganisation(
        mo_code=5902, mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ БОЛЬНИЦА № 6"'
    ),
    MedicalOrganisation(
        mo_code=5903,
        mo_name=r'ГБУЗ СО "САМАРСКАЯ ГОРОДСКАЯ ПОЛИКЛИНИКА № 10 СОВЕТСКОГО РАЙОНА"',
    ),
    MedicalOrganisation(
        mo_code=5905, mo_name=r"ГБУЗ СО САМАРСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА № 3"
    ),
    MedicalOrganisation(
        mo_code=6001, mo_name=r"МИНИСТЕРСТВО ЗДРАВООХРАНЕНИЯ САМАРСКОЙ ОБЛАСТИ"
    ),
    MedicalOrganisation(
        mo_code=6002,
        mo_name=r"ГБУЗ САМАРСКАЯ ОБЛАСТНАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА ИМ. В.Д.СЕРЕДАВИНА",
    ),
    MedicalOrganisation(mo_code=6003, mo_name=r'АО "САМАРСКИЙ ДИАГНОСТИЧЕСКИЙ ЦЕНТР"'),
    MedicalOrganisation(
        mo_code=6004, mo_name=r"ГБУЗ САМАРСКАЯ ОБЛАСТНАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА № 2"
    ),
    MedicalOrganisation(
        mo_code=6005,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ МЕДИЦИНСКИЙ ИНФОРМАЦИОННО-АНАЛИТИЧЕСКИЙ ЦЕНТР",
    ),
    MedicalOrganisation(
        mo_code=6007,
        mo_name=r"ГБУЗ САМАРСКАЯ ОБЛАСТНАЯ КЛИНИЧЕСКАЯ ОФТАЛЬМОЛОГИЧЕСКАЯ БОЛЬНИЦА ИМЕНИ Т.И. ЕРОШЕВСКОГО",
    ),
    MedicalOrganisation(
        mo_code=6008,
        mo_name=r"ГБУЗ САМАРСКАЯ ОБЛАСТНАЯ КЛИНИЧЕСКАЯ ПСИХИАТРИЧЕСКАЯ БОЛЬНИЦА",
    ),
    MedicalOrganisation(
        mo_code=6009,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ КЛИНИЧЕСКИЙ ЦЕНТР  ПРОФИЛАКТИКИ И  БОРЬБЫ СО СПИД",
    ),
    MedicalOrganisation(
        mo_code=6010,
        mo_name=r"ГБУЗ САМАРСКАЯ ОБЛАСТНАЯ КЛИНИЧЕСКАЯ СТОМАТОЛОГИЧЕСКАЯ ПОЛИКЛИНИКА",
    ),
    MedicalOrganisation(
        mo_code=6011,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ КЛИНИЧЕСКИЙ ГОСПИТАЛЬ ДЛЯ ВЕТЕРАНОВ ВОЙН ИМЕНИ О.Г. ЯКОВЛЕВА",
    ),
    MedicalOrganisation(
        mo_code=6013,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ КЛИНИЧЕСКИЙ ПРОТИВОТУБЕРКУЛЕЗНЫЙ ДИСПАНСЕР ИМ.Н.В.ПОСТНИКОВА",
    ),
    MedicalOrganisation(
        mo_code=6015,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ КОЖНО-ВЕНЕРОЛОГИЧЕСКИЙ ДИСПАНСЕР",
    ),
    MedicalOrganisation(
        mo_code=6016,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ КЛИНИЧЕСКИЙ ОНКОЛОГИЧЕСКИЙ ДИСПАНСЕР",
    ),
    MedicalOrganisation(
        mo_code=6017,
        mo_name=r"ГБУЗ САМАРСКАЯ ОБЛАСТНАЯ КЛИНИЧЕСКАЯ СТАНЦИЯ ПЕРЕЛИВАНИЯ КРОВИ",
    ),
    MedicalOrganisation(
        mo_code=6018, mo_name=r"ФБУЗ ЦЕНТР ГИГИЕНЫ И ЭПИДЕМИОЛОГИИ В САМАРСКОЙ ОБЛАСТИ"
    ),
    MedicalOrganisation(
        mo_code=6019,
        mo_name=r'ГБУЗ "САМАРСКИЙ ОБЛАСТНОЙ ЦЕНТР ОБЩЕСТВЕННОГО ЗДОРОВЬЯ И МЕДИЦИНСКОЙ ПРОФИЛАКТИКИ "',
    ),
    MedicalOrganisation(
        mo_code=6020,
        mo_name=r"ГБУЗ САМАРСКОЕ ОБЛАСТНОЕ БЮРО СУДЕБНО-МЕДИЦИНСКОЙ ЭКСПЕРТИЗЫ",
    ),
    MedicalOrganisation(
        mo_code=6021,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ КЛИНИЧЕСКИЙ КАРДИОЛОГИЧЕСКИЙ ДИСПАНСЕР ИМ. В.П. ПОЛЯКОВА",
    ),
    MedicalOrganisation(
        mo_code=6023, mo_name=r'ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ ДЕТСКИЙ САНАТОРИЙ "ЮНОСТЬ"'
    ),
    MedicalOrganisation(
        mo_code=6025,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ КЛИНИЧЕСКИЙ НАРКОЛОГИЧЕСКИЙ ДИСПАНСЕР",
    ),
    MedicalOrganisation(
        mo_code=6028,
        mo_name=r"ГБУЗ САМАРСКИЙ ОБЛАСТНОЙ ЦЕНТР МЕДИЦИНЫ КАТАСТРОФ И СКОРОЙ МЕДПОМОЩИ",
    ),
    MedicalOrganisation(
        mo_code=6029,
        mo_name=r'ГКУЗ САМАРСКИЙ ОБЛАСТНОЙ МЕДЦЕНТР МОБИЛИЗАЦИОННЫХ РЕЗЕРВОВ "РЕЗЕРВ"',
    ),
    MedicalOrganisation(mo_code=6030, mo_name=r"ГБУЗ СО МЕДИЦИНСКИЙ ЦЕНТР ДИНАСТИЯ"),
    MedicalOrganisation(
        mo_code=6032,
        mo_name=r"ГБУЗ ЦЕНТР КОНТРОЛЯ КАЧЕСТВА ЛЕКАРСТВЕННЫХ СРЕДСТВ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=6034, mo_name=r'ГБУ СО "ЦЕНТР УТИЛИЗАЦИИ МЕДИЦИНСКИХ ОТХОДОВ"'
    ),
    MedicalOrganisation(mo_code=6036, mo_name=r"ГБУЗ СО ТОЛЬЯТТИНСКАЯ ДЕЗСТАНЦИЯ"),
    MedicalOrganisation(
        mo_code=7001,
        mo_name=r"ТЕРРИТОРИАЛЬНЫЙ ФОНД ОБЯЗАТЕЛЬНОГО МЕДИЦИНСКОГО СТРАХОВАНИЯ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(mo_code=7101, mo_name=r"СЧЕТНАЯ ПАЛАТА САМАРСКОЙ ОБЛАСТИ"),
    MedicalOrganisation(
        mo_code=9001, mo_name=r'ЧУЗ "КЛИНИЧЕСКАЯ БОЛЬНИЦА "РЖД-МЕДИЦИНА" ГОРОДА САМАРА"'
    ),
    MedicalOrganisation(mo_code=9101, mo_name=r'ООО "АЛЬЯНС"'),
    MedicalOrganisation(mo_code=9102, mo_name=r'УФП СО САНАТОРИЙ "КРАСНАЯ ГЛИНКА"'),
    MedicalOrganisation(mo_code=9103, mo_name=r'ОАО "САНАТОРИЙ ИМ. В.П.ЧКАЛОВА"'),
    MedicalOrganisation(
        mo_code=9104, mo_name=r'ФГБУЗ МРЦ "СЕРГИЕВСКИЕ МИНЕРАЛЬНЫЕ ВОДЫ" ФМБА РОССИИ'
    ),
    MedicalOrganisation(mo_code=9112, mo_name=r'САНАТОРИЙ "ВОЛЖСКИЙ УТЕС"'),
    MedicalOrganisation(
        mo_code=9113, mo_name=r'МП ГО САМАРА "ТТУ" САНАТОРИЙ-ПРОФИЛАКТОРИЙ'
    ),
    MedicalOrganisation(mo_code=9139, mo_name=r'ООО "САНАТОРИЙ "СВЕЖЕСТЬ" (Г.СЫЗРАНЬ)'),
    MedicalOrganisation(mo_code=9144, mo_name=r'ООО САНАТОРИЙ "НЕФТЯНИК"'),
    MedicalOrganisation(mo_code=9148, mo_name=r'МАУ САНАТОРИЙ "МОЛОДЕЦКИЙ КУРГАН"'),
    MedicalOrganisation(mo_code=9150, mo_name=r'ФГБУ "СКК "ПРИВОЛЖСКИЙ" МО РФ'),
    MedicalOrganisation(
        mo_code=9201,
        mo_name=r"ГБУ СО СОЛНЕЧНО-ПОЛЯНСКИЙ ПАНСИОНАТ МИЛОСЕРДИЯ ДЛЯ ИНВАЛИДОВ",
    ),
    MedicalOrganisation(
        mo_code=9202, mo_name=r"ГБУ СО КРАСНОАРМЕЙСКИЙ СПЕЦИАЛЬНЫЙ ПАНСИОНАТ"
    ),
    MedicalOrganisation(
        mo_code=9204, mo_name=r"ГБУ СО ВЛАДИМИРОВСКИЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9205, mo_name=r"ГБУ СО ПОТАПОВСКИЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9207, mo_name=r"ГБУ СО СЫЗРАНСКИЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9208,
        mo_name=r"ГБУ СО ПОХВИСТНЕВСКИЙ МОЛОДЕЖНЫЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ",
    ),
    MedicalOrganisation(
        mo_code=9209, mo_name=r'ГБУ СО "САМАРСКИЙ МОЛОДЕЖНЫЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ"'
    ),
    MedicalOrganisation(
        mo_code=9210, mo_name=r"ГБУ СО САМАРСКИЙ ПАНСИОНАТ № 2 ДЛЯ ДЕТЕЙ-ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9211, mo_name=r"ГБУ СО САМАРСКИЙ ОБЛАСТНОЙ ГЕРОНТОЛОГИЧЕСКИЙ ЦЕНТР"
    ),
    MedicalOrganisation(
        mo_code=9212, mo_name=r"ГБУ СО БАХИЛОВСКИЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9213, mo_name=r"ГБУ СО ВЫСОКИНСКИЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9214, mo_name=r"ГБУ СО СЫЗРАНСКИЙ ГЕРОНТОПСИХИАТРИЧЕСКИЙ ЦЕНТР"
    ),
    MedicalOrganisation(
        mo_code=9215, mo_name=r"ГБУ СО СЕРГИЕВСКИЙ ПАНСИОНАТ ДЛЯ ДЕТЕЙ-ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9217, mo_name=r"ГБУ СО ТОЛЬЯТТИНСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ТРУДА"
    ),
    MedicalOrganisation(
        mo_code=9218,
        mo_name=r"ГБУ СО БОЛЬШЕ-ГЛУШИЦКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9220,
        mo_name=r"ГБУ СО ХВОРОСТЯНСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9221,
        mo_name=r"ГБУ СО ДУБОВО-УМЕТСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9222,
        mo_name=r"ГБУ СО КИНЕЛЬ-ЧЕРКАССКИЙ ПАНСИОНАТ МИЛОСЕРДИЯ ДЛЯ ВЕТЕРАНОВ ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9223, mo_name=r"ГБУ СО ПРИВОЛЖСКИЙ МОЛОДЕЖНЫЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9228,
        mo_name=r"ГБУ СО ОТРАДНЕНСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9230,
        mo_name=r"ГБУ СО ШЕНТАЛИНСКИЙ ПАНСИОНАТ МИЛОСЕРДИЯ ДЛЯ ВЕТЕРАНОВ ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9231, mo_name=r"ГБУ СО СЫЗРАНСКИЙ ПАНСИОНАТ МИЛОСЕРДИЯ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9233, mo_name=r"ГБУ СО ЧАПАЕВСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ТРУДА"
    ),
    MedicalOrganisation(
        mo_code=9234, mo_name=r"ГБУ СО МАКСИМОВСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ТРУДА"
    ),
    MedicalOrganisation(
        mo_code=9236,
        mo_name=r"ГБУ СО ИСАКЛИНСКИЙ ПАНСИОНАТ МИЛОСЕРДИЯ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9237,
        mo_name=r"ГБУ СО АЛЕКСЕЕВСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9238,
        mo_name=r"ГБУ СО СЕРГИЕВСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9239,
        mo_name=r"ГБУ СО КЛЯВЛИНСКИЙ ПАНСИОНАТ МИЛОСЕРДИЯ ДЛЯ ВЕТЕРАН.ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9240,
        mo_name=r"ГБУ СО ОКТЯБРЬСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9241, mo_name=r"ГБУ СО КОШКИНСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ТРУДА"
    ),
    MedicalOrganisation(
        mo_code=9242, mo_name=r"ГБУ СО ПЕСТРАВСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ТРУДА"
    ),
    MedicalOrganisation(
        mo_code=9244,
        mo_name=r"ГБУ СО ЖИГУЛЕВСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ВОЙНЫ И ТРУДА",
    ),
    MedicalOrganisation(
        mo_code=9245, mo_name=r"ГБУ СО БОРСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ТРУДА"
    ),
    MedicalOrganisation(
        mo_code=9246, mo_name=r"ГБУ СО ЧЕЛНО-ВЕРШИНСКИЙ ПАНСИОНАТ ДЛЯ ВЕТЕРАНОВ ТРУДА"
    ),
    MedicalOrganisation(
        mo_code=9247,
        mo_name=r"ГКУ СО ЦЕНТР СОЦИАЛЬНОЙ АДАПТАЦИИ ДЛЯ ЛИЦ БЕЗ ОПРЕДЕЛЕН.МЕСТА ЖИТЕЛЬСТ.И ЗАНЯТИЙ",
    ),
    MedicalOrganisation(
        mo_code=9249, mo_name=r'ГБУ СО СОЦИАЛЬНО-ОЗДОРОВИТЕЛЬНЫЙ ЦЕНТР "ДОБЛЕСТЬ"'
    ),
    MedicalOrganisation(
        mo_code=9251, mo_name=r"ГУ СО ТИМАШЕВСКИЙ ПАНСИОНАТ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(mo_code=9252, mo_name=r"ГБУЗ СО САНАТОРИЙ САМАРА Г.КИСЛОВОДСК"),
    MedicalOrganisation(
        mo_code=9253, mo_name=r"ГБУ СО ШИГОНСКИЙ ПАНСИОНАТ МИЛОСЕРДИЯ ДЛЯ ИНВАЛИДОВ"
    ),
    MedicalOrganisation(
        mo_code=9256,
        mo_name=r'ГБУ СО СОЦИАЛЬНО-ОЗДОРОВИТЕЛЬНЫЙ ЦЕНТР "НОВОКУЙБЫШЕВСКИЙ"',
    ),
    MedicalOrganisation(
        mo_code=9257, mo_name=r'ГБУ СО СОЦИАЛЬНО-ОЗДОРОВИТЕЛЬНЫЙ ЦЕНТР "ПРЕОДОЛЕНИЕ"'
    ),
    MedicalOrganisation(
        mo_code=9258,
        mo_name=r'ГБУ СО СОЦИАЛЬНЫЙ РЕАБИЛИТАЦИОННЫЙ ЦЕНТР ДЛЯ ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ "ИППОТЕРАПИЯ"',
    ),
    MedicalOrganisation(mo_code=9260, mo_name=r"ГБУ СО СУРДОЦЕНТР САМАРСКОЙ ОБЛАСТИ"),
    MedicalOrganisation(
        mo_code=9280,
        mo_name=r'ГБУ СО СОЦИАЛЬНО-РЕАБИЛИТАЦИОННЫЙ ЦЕНТР ДЛЯ ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ "САМАРСКИЙ"',
    ),
    MedicalOrganisation(
        mo_code=9301, mo_name=r"ФКУЗ МСЧ МВД РОССИИ ПО САМАРСКОЙ ОБЛАСТИ"
    ),
    MedicalOrganisation(
        mo_code=9328,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР КОШКИНСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9329,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР АЛЕКСЕЕВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9330,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР ВОЛЖСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9331,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР КИНЕЛЬСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9332,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ГО ОТРАДНЫЙ",
    ),
    MedicalOrganisation(
        mo_code=9333,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР БОГАТОВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9334,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР ХВОРОСТЯНСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9335,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР КРАСНОЯРСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9336,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР СЫЗРАНСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9337,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ГО ПОХВИСТНЕВО",
    ),
    MedicalOrganisation(
        mo_code=9342,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР СЕРГИЕВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9352,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР НЕФТЕГОРСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9357,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР ЧЕЛНО-ВЕРШИНСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9358,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР ПЕСТРАВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9359,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ГО СЫЗРАНЬ",
    ),
    MedicalOrganisation(
        mo_code=9360,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР ПОХВИСТНЕВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9362,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ГО ЧАПАЕВСК",
    ),
    MedicalOrganisation(
        mo_code=9363,
        mo_name=r'ГБУ СО ЦЕНТР ДНЕВНОГО ПРЕБЫВ.ГРАЖДАН ПОЖИЛ.ВОЗРАСТА И ИНВАЛИДОВ "ЗДОРОВЬЕ"',
    ),
    MedicalOrganisation(
        mo_code=9364,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР КИНЕЛЬ-ЧЕРКАССКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9365,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ Ж/ДОРОЖ.Р-НА ГО САМАРА",
    ),
    MedicalOrganisation(
        mo_code=9366,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ КИРОВСКОГО Р-НА ГО САМАРА",
    ),
    MedicalOrganisation(
        mo_code=9367,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ КРАСНОГЛ.Р-НА ГО САМАРА",
    ),
    MedicalOrganisation(
        mo_code=9368,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ КУЙБЫШЕВ. Р-НА ГО САМАРА",
    ),
    MedicalOrganisation(
        mo_code=9370,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ОКТЯБРЬСК. Р-НА ГО САМАРА",
    ),
    MedicalOrganisation(
        mo_code=9372,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ САМАРСКОГО Р-НА ГО САМАРА",
    ),
    MedicalOrganisation(
        mo_code=9373,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ СОВЕТСКОГО Р-НА ГО САМАРА",
    ),
    MedicalOrganisation(
        mo_code=9374,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ АВТОЗАВОД.Р-НА ГО ТОЛЬЯТТИ",
    ),
    MedicalOrganisation(
        mo_code=9375,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ КОМСОМОЛ. Р-НА ГО ТОЛЬЯТТИ",
    ),
    MedicalOrganisation(
        mo_code=9376,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ЦЕНТРАЛ.Р-НА ГО ТОЛЬЯТТИ",
    ),
    MedicalOrganisation(
        mo_code=9377,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ГО ЖИГУЛЕВСК",
    ),
    MedicalOrganisation(
        mo_code=9378,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ГО КИНЕЛЬ",
    ),
    MedicalOrganisation(
        mo_code=9379,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ГО НОВОКУЙБЫШЕВСК",
    ),
    MedicalOrganisation(
        mo_code=9380,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ ГО ОКТЯБРЬСК",
    ),
    MedicalOrganisation(
        mo_code=9381,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР БЕЗЕНЧУКСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9382,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР БОЛЬШЕГЛУШИЦКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9383,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР БОЛЬШЕЧЕРНИГОВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9384,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР БОРСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9385,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР ЕЛХОВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9386,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР ИСАКЛИНСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9388,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР КРАСНОАРМЕЙСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9389,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР ПРИВОЛЖСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9390,
        mo_name=r"ГБУ СО ЦСО ГРАЖДАН ПОЖИЛОГО ВОЗРАСТА И ИНВАЛИДОВ МР СТАВРОПОЛЬСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9394,
        mo_name=r"ГКУ СО ТОЛЬЯТТИНСКИЙ СОЦИАЛЬНЫЙ ПРИЮТ ДЛЯ ЛИЦ БЕЗ ОПРЕДЕЛЕННОГО МЕСТА ЖИТЕЛЬСТВА И ЗАНЯТИЙ",
    ),
    MedicalOrganisation(
        mo_code=9401,
        mo_name=r"ФГБОУ ВО САМАРСКИЙ ГОСУДАРСТВЕННЫЙ МЕДИЦИНСКИЙ УНИВЕРСИТЕТ",
    ),
    MedicalOrganisation(mo_code=9407, mo_name=r'ГКУ СО АЛЕКСЕЕВСКИЙ СРЦН "РАДУГА"'),
    MedicalOrganisation(
        mo_code=9408,
        mo_name=r'ГКУ СО БЕЗЕНЧУКСКИЙ  КОМПЛЕКСНЫЙ ЦЕНТР СОЦ.ОБСЛУЖ.НАСЕЛЕНИЯ "ДОМ ДЕТСТВА"',
    ),
    MedicalOrganisation(mo_code=9409, mo_name=r"ГКУ СО БОЛЬШЕГЛУШИЦКИЙ РЦДПОВ МР"),
    MedicalOrganisation(
        mo_code=9411,
        mo_name=r"МКУ КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ МАТЕРИНСТВА И ДЕТСТВА МР КИНЕЛЬ-ЧЕРКАССКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9412,
        mo_name=r'ГКУ СО "ЦЕНТР "СЕМЬЯ" ВОСТОЧНОГО ОКРУГА" ОТДЕЛЕНИЕ М.Р. КИНЕЛЬ - ЧЕРКАССКИЙ',
    ),
    MedicalOrganisation(mo_code=9413, mo_name=r"МУ ЦЕНТР СЕМЬЯ МР НЕФТЕГОРСКИЙ"),
    MedicalOrganisation(mo_code=9419, mo_name=r'НМУ СРЦН "НАШ ДОМ" ГО НОВОКУЙБЫШЕВСК'),
    MedicalOrganisation(mo_code=9420, mo_name=r"ГКУ СО СРЦН ГО ОКТЯБРЬСК"),
    MedicalOrganisation(mo_code=9421, mo_name=r"ГКУ СО ОТРАДНЕНСКИЙ ЦЕНТР СЕМЬЯ"),
    MedicalOrganisation(mo_code=9423, mo_name=r'ГКУ СО СРЦН "ОГОНЕК" ГО ОТРАДНЫЙ'),
    MedicalOrganisation(mo_code=9425, mo_name=r"ГКУ СО КИНЕЛЬСКИЙ РЦДПОВ"),
    MedicalOrganisation(
        mo_code=9426, mo_name=r'ГКУ СО "РЦДПОВ "СВЕТЛЯЧОК" ГО НОВОКУЙБЫШЕВСК'
    ),
    MedicalOrganisation(
        mo_code=9427, mo_name=r"МУ ЦЕНТР СЕМЬЯ ЖЕЛЕЗНОДОРОЖНОГО РАЙОНА ГО САМАРА"
    ),
    MedicalOrganisation(
        mo_code=9430,
        mo_name=r'МКУ СОЦИАЛЬНЫЙ ПРИЮТ "РОВЕСНИК" КИРОВСКОГО РАЙОНА ГО САМАРА',
    ),
    MedicalOrganisation(
        mo_code=9433, mo_name=r'МКУ РЦДПОВ "ЖУРАВУШКА" ПРОМЫШЛЕННОГО РАЙОНА ГО САМАРА'
    ),
    MedicalOrganisation(
        mo_code=9434,
        mo_name=r'МКУ СОЦИАЛЬНЫЙ ПРИЮТ "РАДУГА" КУЙБЫШЕВСКОГО РАЙОНА ГО САМАРА',
    ),
    MedicalOrganisation(mo_code=9435, mo_name=r"ГКУ СО ОБЛАСТНОЙ РЦДПОВ"),
    MedicalOrganisation(
        mo_code=9437, mo_name=r"МКУ ЦЕНТР СЕМЬЯ СОВЕТСКОГО РАЙОНА ГО САМАРА"
    ),
    MedicalOrganisation(mo_code=9441, mo_name=r"МКУ ЦЕНТР СЕМЬЯ МР ИСАКЛИНСКИЙ"),
    MedicalOrganisation(mo_code=9443, mo_name=r'МКУ СРЦН "РОДНИЧОК" МР СТАВРОПОЛЬСКИЙ'),
    MedicalOrganisation(mo_code=9444, mo_name=r'ГКУ СО КРАСНОЯРСКИЙ СРЦН "ФЕНИКС"'),
    MedicalOrganisation(mo_code=9445, mo_name=r"МКУ ЦЕНТР СЕМЬЯ МР КРАСНОЯРСКИЙ"),
    MedicalOrganisation(
        mo_code=9446,
        mo_name=r"ОТДЕЛ ПО ВОПРОСАМ СЕМЬИ, МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТР.МР КРАСНОЯРСКИЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9447,
        mo_name=r"ГКУ СО ШЕНТАЛИНСКИЙ СОЦИАЛЬНЫЙ ПРИЮТ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ",
    ),
    MedicalOrganisation(
        mo_code=9449,
        mo_name=r'ГКУ СО ОБЛАСТНОЙ СОЦИАЛЬНЫЙ ПРИЮТ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ "НАДЕЖДА"',
    ),
    MedicalOrganisation(
        mo_code=9450,
        mo_name=r"ГКУ СО ОБЛАСТНОЙ ЦЕНТР ПО ОРГАНИЗАЦИИ ОТДЫХА И ОЗДОРОВЛЕНИЯ ДЕТЕЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9452, mo_name=r'ГКУ СРЦН "СОЛНЕЧНЫЙ ЛУЧИК" МР ПРИВОЛЖСКИЙ'
    ),
    MedicalOrganisation(
        mo_code=9453,
        mo_name=r"ГКУ СО ХВОРОСТЯНСКИЙ СОЦИАЛЬНЫЙ ПРИЮТ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ",
    ),
    MedicalOrganisation(
        mo_code=9456,
        mo_name=r"ГКУ СО СОЦИАЛЬНАЯ ГОСТИНИЦА ДЛЯ БЕРЕМЕННЫХ ЖЕНЩИН И ЖЕНЩИН С ДЕТЬМИ МР СЕРГИЕВСКИЙ",
    ),
    MedicalOrganisation(mo_code=9458, mo_name=r"ГКУ СО ЧАПАЕВСКИЙ СРЦН"),
    MedicalOrganisation(
        mo_code=9459, mo_name=r'ГКУ СО КИНЕЛЬ-ЧЕРКАССКИЙ СРЦН "СОЛНЕЧНЫЙ"'
    ),
    MedicalOrganisation(mo_code=9460, mo_name=r'ГКУ СО ВОЛЖСКИЙ СРЦН "ТОПОЛЕК"'),
    MedicalOrganisation(
        mo_code=9461,
        mo_name=r'ГКУ СО КЛЯВЛИНСКИЙ СОЦИАЛЬНЫЙ ПРИЮТ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ "НАДЕЖДА"',
    ),
    MedicalOrganisation(
        mo_code=9464, mo_name=r"ГБУ СО ОБЛАСТНОЙ ЦЕНТР ДИАГНОСТИКИ И КОНСУЛЬТИРОВАНИЯ"
    ),
    MedicalOrganisation(mo_code=9465, mo_name=r"МУ ТРЦДПОВ МР СЫЗРАНСКИЙ"),
    MedicalOrganisation(mo_code=9468, mo_name=r"МУ ЦЕНТР СЕМЬЯ ГО ЖИГУЛЕВСК"),
    MedicalOrganisation(mo_code=9469, mo_name=r"МУ ЦЕНТР СЕМЬЯ ГО ОКТЯБРЬСК"),
    MedicalOrganisation(mo_code=9471, mo_name=r"МУ ГОРОДСКОЙ ЦЕНТР СЕМЬЯ ГО КИНЕЛЬ"),
    MedicalOrganisation(mo_code=9472, mo_name=r"МКУ ЦЕНТР СЕМЬЯ ГО ПОХВИСТНЕВО"),
    MedicalOrganisation(
        mo_code=9475, mo_name=r"МБУ РАЙОННЫЙ ЦЕНТР СЕМЬЯ МР БЕЗЕНЧУКСКИЙ"
    ),
    MedicalOrganisation(
        mo_code=9476,
        mo_name=r"ГКУ СО БОГАТОВСКИЙ СОЦИАЛЬНЫЙ ПРИЮТ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ",
    ),
    MedicalOrganisation(
        mo_code=9477, mo_name=r"МКУ РАЙОННЫЙ ЦЕНТР СЕМЬЯ МР БОГАТОВСКИЙ"
    ),
    MedicalOrganisation(mo_code=9478, mo_name=r"МУ УСЗН МР БОЛЬШЕГЛУШИЦКИЙ"),
    MedicalOrganisation(mo_code=9479, mo_name=r"МУ ЦЕНТР СЕМЬЯ МР БОЛЬШЕГЛУШИЦКИЙ"),
    MedicalOrganisation(mo_code=9480, mo_name=r"МУ ЦЕНТР СЕМЬЯ МР БОЛЬШЕЧЕРНИГОВСКИЙ"),
    MedicalOrganisation(
        mo_code=9481,
        mo_name=r'ГКУ СО БОРСКИЙ СОЦИАЛЬНЫЙ ПРИЮТ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ "ПОЛЯНКА"',
    ),
    MedicalOrganisation(mo_code=9485, mo_name=r"МБУ ЦЕНТР СЕМЬЯ МР КОШКИНСКИЙ"),
    MedicalOrganisation(mo_code=9487, mo_name=r"ГКУ СО КЛЯВЛИНСКИЙ СРЦДПОВ"),
    MedicalOrganisation(mo_code=9488, mo_name=r"МУ ЦЕНТР СЕМЬЯ МР КЛЯВЛИНСКИЙ"),
    MedicalOrganisation(
        mo_code=9490, mo_name=r"МУ ТЕРРИТОРИАЛЬНЫЙ ЦЕНТР СЕМЬЯ МР ПЕСТРАВСКИЙ"
    ),
    MedicalOrganisation(
        mo_code=9491, mo_name=r"МУ ТЕРРИТОРИАЛЬНЫЙ ЦЕНТР СЕМЬЯ МР ПОХВИСТНЕВСКИЙ"
    ),
    MedicalOrganisation(mo_code=9492, mo_name=r"ГКУ СО ПРИВОЛЖСКИЙ ЦЕНТР СЕМЬЯ"),
    MedicalOrganisation(mo_code=9494, mo_name=r"ГКУ СО СЕРГИЕВСКИЙ РЦДПОВ"),
    MedicalOrganisation(mo_code=9495, mo_name=r"ГКУ СО СЕРГИЕВСКИЙ ЦЕНТР СЕМЬЯ"),
    MedicalOrganisation(
        mo_code=9496, mo_name=r"ГКУ СО СЫЗРАНСКИЙ РАЙОННЫЙ ЦЕНТР СЕМЬЯ"
    ),
    MedicalOrganisation(mo_code=9498, mo_name=r"МУ ЦЕНТР СЕМЬЯ МР ЧЕЛНО-ВЕРШИНСКИЙ"),
    MedicalOrganisation(mo_code=9499, mo_name=r"МУ ЦЕНТР СЕМЬЯ МР ШЕНТАЛИНСКИЙ"),
    MedicalOrganisation(mo_code=9500, mo_name=r"ГКУ СО ШИГОНСКИЙ ЦЕНТР СЕМЬЯ"),
    MedicalOrganisation(mo_code=9502, mo_name=r"ГКУ СО КАМЫШЛИНСКИЙ ЦЕНТР СЕМЬЯ"),
    MedicalOrganisation(
        mo_code=9503, mo_name=r"МУ ТЕРРИТОРИАЛЬНЫЙ ЦЕНТР СЕМЬЯ МР ЕЛХОВСКИЙ"
    ),
    MedicalOrganisation(
        mo_code=9504, mo_name=r"МУ ТЕРРИТОРИАЛЬНЫЙ ЦЕНТР СЕМЬЯ ГО НОВОКУЙБЫШЕВСК"
    ),
    MedicalOrganisation(
        mo_code=9507,
        mo_name=r'ГКУ СО КОМПЛЕКСНЫЙ ЦЕНТР СОЦИАЛЬН.ОБСЛУЖИВ.НАСЕЛЕНИЯ "ЖЕМЧУЖИНА" ГО СЫЗРАНЬ',
    ),
    MedicalOrganisation(
        mo_code=9508, mo_name=r"ГКУ СО СЫЗРАНСКИЙ ГОРОДСКОЙ ЦЕНТР СЕМЬЯ"
    ),
    MedicalOrganisation(mo_code=9509, mo_name=r"МБУ ЦЕНТР СЕМЬЯ ГО ЧАПАЕВСК"),
    MedicalOrganisation(mo_code=9510, mo_name=r'ГКУ СО ЧАПАЕВСКИЙ РЦДПОВ "НАДЕЖДА"'),
    MedicalOrganisation(mo_code=9511, mo_name=r"МКУ ЦЕНТР СЕМЬЯ МР СТАВРОПОЛЬСКИЙ"),
    MedicalOrganisation(mo_code=9512, mo_name=r"МУ ЦЕНТР СЕМЬЯ ГО ТОЛЬЯТТИ"),
    MedicalOrganisation(
        mo_code=9513, mo_name=r"МКУ ЦЕНТР СЕМЬЯ АВТОЗАВОДСКОГО РАЙОНА ГО ТОЛЬЯТТИ"
    ),
    MedicalOrganisation(
        mo_code=9514, mo_name=r"МУ ЦЕНТР СЕМЬЯ КОМСОМОЛЬСКОГО РАЙОНА ГО ТОЛЬЯТТИ"
    ),
    MedicalOrganisation(
        mo_code=9515, mo_name=r"МКУ ЦЕНТР СЕМЬЯ ЦЕНТРАЛЬНОГО РАЙОНА ГО ТОЛЬЯТТИ"
    ),
    MedicalOrganisation(mo_code=9516, mo_name=r'ГКУ СО ТОЛЬЯТТИНСКИЙ СРЦН "ГАРМОНИЯ"'),
    MedicalOrganisation(mo_code=9517, mo_name=r'ГКУ СО ТОЛЬЯТТИНСКИЙ СПДП "ДЕЛЬФИН"'),
    MedicalOrganisation(mo_code=9518, mo_name=r'ГКУ СО РЦДПОВ "ВИКТОРИЯ" ГО ТОЛЬЯТТИ'),
    MedicalOrganisation(mo_code=9521, mo_name=r"ГБУ СО ОБЛАСТНОЙ ЦЕНТР СЕМЬЯ"),
    MedicalOrganisation(mo_code=9522, mo_name=r"МКУ ГОРОДСКОЙ ЦЕНТР СЕМЬЯ ГО САМАРА"),
    MedicalOrganisation(mo_code=9524, mo_name=r"МУ РАЙОННЫЙ ЦЕНТР СЕМЬЯ МР ВОЛЖСКИЙ"),
    MedicalOrganisation(
        mo_code=9525, mo_name=r"МКУ ЦЕНТР СЕМЬЯ ПРОМЫШЛЕННОГО РАЙОНА ГО САМАРА"
    ),
    MedicalOrganisation(
        mo_code=9528,
        mo_name=r"ОТДЕЛ ПО ДЕЛАМ СЕМЬИ,ОХРАНЕ ПРАВ МАТЕРИНСТВА И ДЕТСТВА АДМИН.МР КОШКИНСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9529,
        mo_name=r"ДЕПАРТАМЕНТ СЕМЬИ, ОПЕКИ И ПОПЕЧИТЕЛЬСТВА АДМИНИСТРАЦИИ ГО САМАРА",
    ),
    MedicalOrganisation(
        mo_code=9530,
        mo_name=r"ДЕПАРТАМЕНТ ПО ВОПРОСАМ СЕМЬИ И ДЕМОГРАФИЧЕСКОГО РАЗВИТИЯ МЭРИИ ГО ТОЛЬЯТТИ",
    ),
    MedicalOrganisation(
        mo_code=9535,
        mo_name=r"МУ КОМИТЕТ ПО ВОПРОСАМ ДЕМОГРАФИИ,ОПЕКИ И ПОПЕЧИТ.ГО ОТРАДНЫЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9536,
        mo_name=r"ОТДЕЛ СЕМЬИ, МАТЕРИНСТВА И ДЕТСТВА УПРАВЛЕНИЯ СОЦИАЛЬН.РАЗВИТИЯ АДМИН.ГО ПОХВИСТНЕВО",
    ),
    MedicalOrganisation(
        mo_code=9537,
        mo_name=r"УПРАВЛЕНИЕ ПО ВОПРОСАМ СЕМЬИ МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТРАЦИИ ГО СЫЗРАНЬ",
    ),
    MedicalOrganisation(
        mo_code=9539,
        mo_name=r"КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТРАЦИИ МР АЛЕКСЕЕВСКИЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9541,
        mo_name=r"КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ,МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТРАЦИИ МР БОГАТОВСКИЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9543,
        mo_name=r"МУ УПРАВЛЕНИЕ ПО ВОПРОСАМ СЕМЬИ И ДЕМОГРАФИИ АДМИНИСТРАЦИИ МР БОЛЬШЕЧЕРНИГОВСКИЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9544,
        mo_name=r"МУ КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ,ОПЕКИ И ПОПЕЧИТЕЛЬСТВА МР БОРСКИЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9545,
        mo_name=r"ОТДЕЛ ПО ДЕЛАМ СЕМЬИ,МАТЕРИНСТВА И ДЕТСТВА МР ВОЛЖСКИЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9546,
        mo_name=r"МУ УПРАВЛЕНИЕ ПО ВОПРОСАМ СЕМЬИ И ДЕМОГРАФИИ МР ЕЛХОВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9547,
        mo_name=r"КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ,МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТРАЦИИ МР ИСАКЛИНСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9551,
        mo_name=r"КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ,МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТР.МР КРАСНОАРМЕЙСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9552,
        mo_name=r"УПРАВЛЕНИЕ ПО ВОПРОСАМ СЕМЬИ И ДЕМОГРАФИЧЕСКОГО РАЗВИТИЯ МР НЕФТЕГОРСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9553,
        mo_name=r"КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ,МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТР.МР ПЕСТРАВСКИЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9554,
        mo_name=r"ОТДЕЛ ПО ВОПРОСАМ СЕМЬИ,МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТР.МР ПОХВИСТНЕВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9556,
        mo_name=r"КОМИТЕТ ПО ДЕЛАМ СЕМЬИ И ДЕТСТВА АДМИНИСТРАЦИИ МР СЕРГИЕВСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9557,
        mo_name=r"МУ СЛУЖБА СЕМЬИ,ДЕМОГРАФИЧЕСКОГО РАЗВИТИЯ И ЗАЩИТЫ ПРАВ НЕСОВЕРШЕННОЛЕТНИХ",
    ),
    MedicalOrganisation(
        mo_code=9558,
        mo_name=r"МУ КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ,МАТЕРИНСТВА И ДЕТСТВА ХВОРОСТЯНСКОГО РАЙОНА САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9559,
        mo_name=r"КОМИТЕТ ПО ВОПРОСАМ СЕМЬИ АДМИНИСТРАЦИИ МР ЧЕЛНО-ВЕРШИНСКИЙ САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9560,
        mo_name=r"МУ ОТДЕЛ ПО ВОПРОСАМ СЕМЬИ,МАТЕРИНСТВА И ДЕТСТВА АДМИНИСТРАЦИИ МР ШЕНТАЛИНСКИЙ",
    ),
    MedicalOrganisation(
        mo_code=9601,
        mo_name=r'ФГБОУ ВО "САМАРСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ"',
    ),
    MedicalOrganisation(
        mo_code=9604, mo_name=r'ФГБУ "426 ВОЕННЫЙ ГОСПИТАЛЬ" МИНОБОРОНЫ РОССИИ'
    ),
    MedicalOrganisation(mo_code=9668, mo_name=r'ООО МЕДИЦИНСКИЙ ЦЕНТР "ЗДОРОВЫЕ ДЕТИ"'),
    MedicalOrganisation(mo_code=9669, mo_name=r'ООО МСЧ "ЗИТ"'),
    MedicalOrganisation(mo_code=9670, mo_name=r'АО "ТОЛЬЯТТИАЗОТ"'),
    MedicalOrganisation(
        mo_code=9696,
        mo_name=r"ФГБУ ФЕДЕРАЛЬНЫЙ НАУЧНО-КЛИНИЧЕСКИЙ ЦЕНТР МЕДИЦИНСКОЙ РАДИОЛОГИИ И ОНКОЛОГИИ ФМБА РОССИИ",
    ),
    MedicalOrganisation(
        mo_code=9704, mo_name=r"ФКУ ЛИУ-4  ГУФСИН РОССИИ ПО САМАРСКОЙ ОБЛАСТИ"
    ),
    MedicalOrganisation(
        mo_code=9705, mo_name=r"ФКУ СИЗО-2  ГУФСИН РОССИИ ПО САМАРСКОЙ ОБЛАСТИ"
    ),
    MedicalOrganisation(
        mo_code=9706,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 6 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9707,
        mo_name=r"ФКУ ЖИГУЛЕВСКАЯ ВОСПИТАТЕЛЬНАЯ КОЛОНИЯ ГУФСИН РОССИИ ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9708, mo_name=r"ФКУ СИЗО-3 ГУФСИН РОССИИ ПО САМАРСКОЙ ОБЛАСТИ"
    ),
    MedicalOrganisation(
        mo_code=9709,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 5 ГУФСИН РОССИИ ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9711, mo_name=r"ФКУ СИЗО-1 ГУФСИН РОССИИ ПО САМАРСКОЙ ОБЛАСТИ"
    ),
    MedicalOrganisation(
        mo_code=9712,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 15 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9713,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 13 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9714,
        mo_name=r"ФКЛПУ ОБЛАСТНАЯ ТУБЕРКУЛЕЗНАЯ БОЛЬНИЦА ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9715,
        mo_name=r"ГЛАВНОЕ УПРАВЛЕНИЕ ФЕДЕРАЛЬНОЙ СЛУЖБЫ ИСПОЛНЕНИЯ НАКАЗАНИЙ",
    ),
    MedicalOrganisation(
        mo_code=9726,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 26 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9728,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 28 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9729,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 29 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9730,
        mo_name=r"ФКЛПУ ОБЛАСТНАЯ СОМАТИЧЕСКАЯ БОЛЬНИЦА ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9731,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 3 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9732,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 10 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(
        mo_code=9733,
        mo_name=r"ФКУ ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ № 16 ГУФСИН ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(mo_code=9734, mo_name=r"ФКУЗ МСЧ-63 ФСИН РОССИИ"),
    MedicalOrganisation(
        mo_code=9800,
        mo_name=r"ФЕДЕРАЛЬНАЯ СЛУЖБА РОССИЙСКОЙ ФЕДЕРАЦИИ ПО КОНТРОЛЮ ЗА ОБОРОТОМ НАРКОТИКОВ ПО САМАРСКОЙ ОБЛАСТИ",
    ),
    MedicalOrganisation(mo_code=10007, mo_name=r'ООО "ДОМАШНИЙ ДОКТОР"'),
    MedicalOrganisation(mo_code=10009, mo_name=r'ООО "МЦ "ДЕТСКИЙ ДОКТОР"'),
    MedicalOrganisation(mo_code=10010, mo_name=r'ООО "МК ТОМОГРАФИЯ"'),
    MedicalOrganisation(mo_code=10024, mo_name=r'ООО "ДЦ "ЭКСПРЕСС +"'),
    MedicalOrganisation(mo_code=10027, mo_name=r'ООО " СГЕОЛАЙН "'),
    MedicalOrganisation(
        mo_code=10030, mo_name=r'ООО "САМАРСКИЙ ЦЕНТР ГЛАЗНОЙ ХИРУРГИИ"'
    ),
    MedicalOrganisation(mo_code=10035, mo_name=r'АО "ЕВРОПЕЙСКИЙ МЕДИЦИНСКИЙ ЦЕНТР"'),
    MedicalOrganisation(
        mo_code=10038,
        mo_name=r'ГБУЗ "ДИАГНОСТИЧЕСКИЙ ЦЕНТР ЛАБОРАТОРНЫХ ИССЛЕДОВАНИЙ ДЗМ"',
    ),
    MedicalOrganisation(mo_code=10065, mo_name=r'ООО "МЕДИЦИНСКАЯ КОМПАНИЯ "РЕАВИЗ"'),
    MedicalOrganisation(mo_code=10080, mo_name=r'ООО "МАСТЕРСЛУХ"'),
    MedicalOrganisation(mo_code=10090, mo_name=r'ООО "ГЕПАТОЛОГ"'),
    MedicalOrganisation(mo_code=10094, mo_name=r'АО "ЛДЦ ИММУНОЛОГИИ И АЛЛЕРГОЛОГИИ"'),
    MedicalOrganisation(mo_code=10095, mo_name=r'АО "МЕДИЦИНСКАЯ КОМПАНИЯ ИДК"'),
    MedicalOrganisation(mo_code=10110, mo_name=r'АО "МОСКОВСКОЕ ПРОП"'),
    MedicalOrganisation(mo_code=10130, mo_name=r'ООО "САМАРСКИЙ ЦЕНТР ФЛЕБОЛОГИИ"'),
    MedicalOrganisation(mo_code=10165, mo_name=r'ООО "АЗБУКА ЗДОРОВЬЯ"'),
    MedicalOrganisation(mo_code=10188, mo_name=r'ООО "ЛИДЕР-ОПТИКА"'),
    MedicalOrganisation(mo_code=10240, mo_name=r'ООО "РЕГИОНАЛЬНЫЙ МЕДИЦИНСКИЙ ЦЕНТР"'),
    MedicalOrganisation(mo_code=10364, mo_name=r'ООО "ТОЧКА ЗРЕНИЯ"'),
    MedicalOrganisation(
        mo_code=10384, mo_name=r'ООО "КОНСУЛЬТАТИВНО-ДИАГНОСТИЧЕСКИЙ МЕДИЦИНСКИЙ ЦЕНТР"'
    ),
    MedicalOrganisation(mo_code=10650, mo_name=r'ООО "ПЭТ-ТЕХНОЛОДЖИ ДИАГНОСТИКА"'),
    MedicalOrganisation(mo_code=10745, mo_name=r'ООО "МЕДГАРД"'),
    MedicalOrganisation(mo_code=10747, mo_name=r'ООО "МЕДИЦИНСКИЙ ЛУЧЕВОЙ ЦЕНТР"'),
    MedicalOrganisation(mo_code=10749, mo_name=r'ООО "ЛДЦ МИБС-САМАРА"'),
    MedicalOrganisation(mo_code=10754, mo_name=r'ООО "КРАСНОГЛИНСКИЙ ДОКТОР"'),
    MedicalOrganisation(mo_code=10767, mo_name=r'УСТРИ "АРАХНА" ТООИВ'),
    MedicalOrganisation(mo_code=10769, mo_name=r'ООО "СИТИЛАБ"'),
    MedicalOrganisation(mo_code=10770, mo_name=r'ООО "ДЕНТЕКС"'),
    MedicalOrganisation(mo_code=10771, mo_name=r'ООО "ДАНТИСТ"'),
    MedicalOrganisation(mo_code=10772, mo_name=r'ООО "МЕДИКАЛ СЕРВИС КОМПАНИ"'),
    MedicalOrganisation(
        mo_code=10774, mo_name=r'ООО "ТОЛЬЯТТИНСКИЙ ДИАГНОСТИЧЕСКИЙ ЦЕНТР № 1"'
    ),
    MedicalOrganisation(mo_code=10776, mo_name=r'ООО "ЦЭИМ"'),
    MedicalOrganisation(mo_code=10777, mo_name=r'ООО "ДИАГНОСТИКА И ЛЕЧЕНИЕ"'),
    MedicalOrganisation(mo_code=10790, mo_name=r'ООО "ЧАСТНЫЙ ОФИС РЯЗАНОВОЙ"'),
    MedicalOrganisation(mo_code=10793, mo_name=r'ООО "НАДЕЖДА"(Железнодорожный)'),
    MedicalOrganisation(mo_code=10799, mo_name=r'ООО "АМИТИС"'),
    MedicalOrganisation(mo_code=10800, mo_name=r'МАУ ДЕТСКИЙ ЦЕНТР "БЕРЕЗКИ"'),
    MedicalOrganisation(
        mo_code=10805, mo_name=r'КЛИНИКА РЕПРОДУКТИВНОГО ЗДОРОВЬЯ "ЭКО" (ООО "СВС")'
    ),
    MedicalOrganisation(mo_code=10806, mo_name=r'ООО "ИНВИТРО-САМАРА"'),
    MedicalOrganisation(mo_code=10813, mo_name=r'ООО "ОТКРЫТЫЙ КОД"'),
    MedicalOrganisation(mo_code=10815, mo_name=r'ООО "ЛДЦ МИБС-ТОЛЬЯТТИ"'),
    MedicalOrganisation(mo_code=10823, mo_name=r'ООО "ЛДЦ МИБС - СЫЗРАНЬ"'),
    MedicalOrganisation(mo_code=10824, mo_name=r'ООО "МЦ "ЗДОРОВЬЕ ДЕТЕЙ"'),
    MedicalOrganisation(mo_code=10825, mo_name=r'МЕДИЦИНСКИЙ УНИВЕРСИТЕТ "РЕАВИЗ"'),
    MedicalOrganisation(mo_code=10830, mo_name=r'ОАО "ВИОЛА"'),
    MedicalOrganisation(mo_code=10835, mo_name=r'ООО "СКАЙЛАБ"'),
    MedicalOrganisation(mo_code=10837, mo_name=r'АНО "САМАРСКИЙ ХОСПИС"'),
    MedicalOrganisation(mo_code=10839, mo_name=r'АНО "ССМП "ЗДОРОВАЯ СЕМЬЯ"'),
    MedicalOrganisation(mo_code=10840, mo_name=r'ООО "ЗДОРОВЫЕ НАСЛЕДНИКИ"'),
    MedicalOrganisation(mo_code=10844, mo_name=r'ООО "ПРОБИР-КА"'),
    MedicalOrganisation(mo_code=10845, mo_name=r'ООО МЦ "ПРОФЛИДЕР"'),
    MedicalOrganisation(
        mo_code=10846,
        mo_name=r'ГАУЗ "РЕСПУБЛИКАНСКАЯ КЛИНИЧЕСКАЯ ОФТАЛЬМОЛОГИЧЕСКАЯ БОЛЬНИЦА МЗ РЕСПУБЛИКИ ТАТАРСТАН"',
    ),
    MedicalOrganisation(mo_code=10852, mo_name=r'ООО "ЦАД 63"'),
    MedicalOrganisation(mo_code=10854, mo_name=r'ООО "КЛИНИКА ДЕНТ"'),
    MedicalOrganisation(mo_code=10858, mo_name=r'ООО "МЕДСЕРВИС"'),
    MedicalOrganisation(mo_code=10875, mo_name=r'ООО "А2МЕД САМАРА"'),
    MedicalOrganisation(mo_code=10880, mo_name=r'ООО "ФАРМЛАЙН-ВОЛГА"'),
    MedicalOrganisation(mo_code=10885, mo_name=r'ООО "НОВЫЕ МЕДИЦИНСКИЕ ТЕХНОЛОГИИ"'),
    MedicalOrganisation(mo_code=10891, mo_name=r'ООО "ЛАБОРАТОРИЯ ГЕМОТЕСТ"'),
    MedicalOrganisation(mo_code=10896, mo_name=r'ООО "ГЕМОТЕСТ САМАРА"'),
    MedicalOrganisation(mo_code=10897, mo_name=r'ООО "МДЦ ЗДОРОВЬЕ"'),
    MedicalOrganisation(mo_code=10898, mo_name=r'ООО "ЛЕГКОЕ ДЫХАНИЕ"'),
    MedicalOrganisation(mo_code=20001, mo_name=r'ООО "РАДУГА"'),
    MedicalOrganisation(mo_code=20002, mo_name=r'ООО "ГИППОКРАТ"'),
    MedicalOrganisation(mo_code=20003, mo_name=r'ООО "ЭЛЬМЕДКЛИНИК"'),
    MedicalOrganisation(mo_code=20004, mo_name=r'ООО "МЕДЭКСПЕРТ"'),
    MedicalOrganisation(mo_code=20005, mo_name=r'ООО "СКОРПИОН"'),
    MedicalOrganisation(mo_code=20006, mo_name=r'ООО "ПРОФМЕДЦЕНТР"'),
    MedicalOrganisation(mo_code=20007, mo_name=r'ООО "ДИАМЕД"'),
    MedicalOrganisation(
        mo_code=20008, mo_name=r'ООО "САМАРСКИЙ СТРАХОВОЙ МЕДИЦИНСКИЙ ЦЕНТР"'
    ),
    MedicalOrganisation(mo_code=20009, mo_name=r'ООО "АСОКМАМЕД"'),
    MedicalOrganisation(mo_code=20010, mo_name=r'ООО "КЛИНИКА ДОКТОРА МУТ"'),
    MedicalOrganisation(mo_code=20011, mo_name=r'ООО МК "МЕДТЕХКОМПЛЕКТ"'),
    MedicalOrganisation(mo_code=20012, mo_name=r'ООО "ЛОР-ПРОФМЕД"'),
    MedicalOrganisation(mo_code=20013, mo_name=r'ООО "ИНРОС-МЕД"'),
    MedicalOrganisation(mo_code=20015, mo_name=r'ООО "МЕДСПРАВКИ 63"'),
    MedicalOrganisation(mo_code=20016, mo_name=r'ООО "ПЕЙСМЕКЕР"'),
    MedicalOrganisation(mo_code=20017, mo_name=r'ООО "МЕДЭКСПРЕСС"'),
    MedicalOrganisation(mo_code=20018, mo_name=r'ООО "ЭКСПЕРТ-ПРОФИТ"'),
    MedicalOrganisation(mo_code=20019, mo_name=r'ООО "ПРОФИМЕД"'),
    MedicalOrganisation(mo_code=20021, mo_name=r'ООО "МЕДГРАД"'),
    MedicalOrganisation(mo_code=20022, mo_name=r'ООО "ВЕГА-С"'),
    MedicalOrganisation(mo_code=20023, mo_name=r'ООО "НОВОКУЙБЫШЕВСК МЕДСПРАВКА"'),
    MedicalOrganisation(mo_code=20024, mo_name=r'ООО "МАШИНЕРИ"'),
    MedicalOrganisation(mo_code=20025, mo_name=r'ООО "ПРИЗВАНИЕ"'),
    MedicalOrganisation(mo_code=20026, mo_name=r'ООО "ГЕНОМ"'),
    MedicalOrganisation(mo_code=20027, mo_name=r'ООО "ИПОТЕЧНЫЙ ДОМ"'),
    MedicalOrganisation(mo_code=20029, mo_name=r'ООО МЦ "ГУБЕРНИЯ"'),
    MedicalOrganisation(mo_code=20030, mo_name=r'ООО "ФРЕЗЕНИУС НЕФРОКЕА"'),
    MedicalOrganisation(mo_code=20032, mo_name=r'ООО "ПОЛИКЛИНИКА+"'),
    MedicalOrganisation(mo_code=20033, mo_name=r'ООО "КЛИНИКА ЕВРАЗИЯ"'),
    MedicalOrganisation(mo_code=20034, mo_name=r'ООО "НАУКА"'),
    MedicalOrganisation(mo_code=20035, mo_name=r'ООО "ПРОФОСМОТР"'),
    MedicalOrganisation(mo_code=20036, mo_name=r'ООО "ИН ПРОМ МЕД"'),
    MedicalOrganisation(mo_code=20037, mo_name=r'ООО "НАУКА КДЛ"'),
    MedicalOrganisation(mo_code=20038, mo_name=r'ООО "НАУКА БАК"'),
    MedicalOrganisation(mo_code=20039, mo_name=r'ООО "МАСТЕР"'),
    MedicalOrganisation(mo_code=20040, mo_name=r"ООО НАУКА ПЦР"),
    MedicalOrganisation(mo_code=20043, mo_name=r'ООО МК "ПРОФЕССИОНАЛ"'),
    MedicalOrganisation(mo_code=20044, mo_name=r'ООО "ДОКТОР ПЛЮС"'),
    MedicalOrganisation(
        mo_code=20100, mo_name=r"УГИБДД ГУ МВД РОССИИ ПО САМАРСКОЙ ОБЛАСТИ"
    ),
    MedicalOrganisation(
        mo_code=20200,
        mo_name=r'ФКУ "ГЛАВНОЕ БЮРО МЕДИКО-СОЦИАЛЬНОЙ ЭКСПЕРТИЗЫ ПО САМАРСКОЙ ОБЛАСТИ"',
    ),
    MedicalOrganisation(mo_code=30001, mo_name=r'ОАО "ФАРМБОКС"'),
    MedicalOrganisation(mo_code=30010, mo_name=r'ООО "АПТЕКА № 302"'),
    MedicalOrganisation(mo_code=30045, mo_name=r'ГУП СО "АПТЕКА № 146"'),
    MedicalOrganisation(mo_code=30057, mo_name=r"ОАО ВИТАФАРМ"),
    MedicalOrganisation(mo_code=30064, mo_name=r'ООО "АПТЕКА № 245"'),
    MedicalOrganisation(mo_code=30082, mo_name=r'ОАО "НОВОФАРМ"'),
    MedicalOrganisation(mo_code=30085, mo_name=r'МУП "АПТЕКА № 168"'),
    MedicalOrganisation(mo_code=30108, mo_name=r"МУП АПТЕКА № 147 С.БОГАТОЕ"),
    MedicalOrganisation(mo_code=30112, mo_name=r'АПТЕКА № 9 ООО "ФАРМАПОЛТОРГ"'),
    MedicalOrganisation(mo_code=30117, mo_name=r'МУП ВОЛЖСКОГО РАЙОНА "АПТЕКА № 105"'),
    MedicalOrganisation(mo_code=30121, mo_name=r'МУП "АПТЕКА № 120"'),
    MedicalOrganisation(mo_code=30153, mo_name=r'МУП "АПТЕКА № 70"'),
    MedicalOrganisation(mo_code=30161, mo_name=r"МАУ ЦРА КРАСНОАРМЕЙСКОГО РАЙОНА"),
    MedicalOrganisation(mo_code=30204, mo_name=r'ООО "ТЭКА"'),
    MedicalOrganisation(mo_code=30206, mo_name=r'ООО "АПТЕКА 222"'),
    MedicalOrganisation(mo_code=30226, mo_name=r'ОАО "АПТЕКА № 21"'),
    MedicalOrganisation(
        mo_code=30227,
        mo_name=r'МУП "ЦЕНТРАЛЬНАЯ РАЙОННАЯ АПТЕКА № 138"ИСАКЛИНСКОГО РАЙОНА',
    ),
    MedicalOrganisation(mo_code=30254, mo_name=r'ООО  "АПТЕКА № 42"'),
    MedicalOrganisation(mo_code=30255, mo_name=r'ООО "МАЙТ"'),
    MedicalOrganisation(mo_code=30257, mo_name=r'ООО "МФК МИЛАНА"'),
    MedicalOrganisation(mo_code=30258, mo_name=r"ИП ХАМИТОВ АНТОН ЮРЬЕВИЧ"),
    MedicalOrganisation(mo_code=30300, mo_name=r'ГКУ СО "САМАРАФАРМАЦИЯ"'),
    MedicalOrganisation(mo_code=30301, mo_name=r'ОАО "ФАРМАЦИЯ" СЕРГИЕВСКОГО РАЙОНА'),
    MedicalOrganisation(mo_code=30302, mo_name=r'ООО "НАША АПТЕКА"'),
    MedicalOrganisation(mo_code=30304, mo_name=r'ООО "РОНА"'),
    MedicalOrganisation(mo_code=30305, mo_name=r'ООО "ФАРМАПОЛ"'),
    MedicalOrganisation(mo_code=30306, mo_name=r'ООО "ФАРМ СКД"'),
    MedicalOrganisation(
        mo_code=30308, mo_name=r'ОО "САМАРСКАЯ ОБЛАСТНАЯ ФАРМАЦЕВТИЧЕСКАЯ АССОЦИАЦИЯ"'
    ),
    MedicalOrganisation(mo_code=30310, mo_name=r'ООО "АРТЕМИДА"'),
    MedicalOrganisation(mo_code=30311, mo_name=r'ООО "ФАРМЛАЙН"'),
    MedicalOrganisation(mo_code=30312, mo_name=r'МУП "АРСЕНАЛ"'),
    MedicalOrganisation(mo_code=30313, mo_name=r'ООО "ФАРМАТЕЛЬ"'),
    MedicalOrganisation(mo_code=30314, mo_name=r'ООО "НАДЕЖДА"(с.Пестравка)'),
    MedicalOrganisation(mo_code=30315, mo_name=r'МУП  "ФАРМАЦИЯ"'),
    MedicalOrganisation(mo_code=30316, mo_name=r'ООО "ВАЛЕО-ФАРМ"'),
    MedicalOrganisation(mo_code=30318, mo_name=r'ООО "АПТЕКА НА ДВОРЯНСКОЙ"'),
    MedicalOrganisation(mo_code=30321, mo_name=r'ООО "ВИТАФАРМ 1"'),
    MedicalOrganisation(mo_code=30322, mo_name=r'ООО "ВИТАПРОФ"'),
    MedicalOrganisation(mo_code=30323, mo_name=r'ООО "АПТЕКА № 236"'),
    MedicalOrganisation(mo_code=30324, mo_name=r'МУП "ПАНАЦЕЯ"'),
    MedicalOrganisation(mo_code=30325, mo_name=r"ИП МАРКОВА ВЕРА МИХАЙЛОВНА"),
    MedicalOrganisation(mo_code=30327, mo_name=r'ООО "МИЛАНА"'),
    MedicalOrganisation(
        mo_code=50004, mo_name=r"ГБПОУ ГУБЕРНСКИЙ КОЛЛЕДЖ Г.ПОХВИСТНЕВО"
    ),
    MedicalOrganisation(
        mo_code=50007, mo_name=r'ГБПОУ "СЫЗРАНСКИЙ МЕДИКО-ГУМАНИТАРНЫЙ КОЛЛЕДЖ"'
    ),
    MedicalOrganisation(
        mo_code=50008, mo_name=r"ГБПОУ ТОЛЬЯТТИНСКИЙ МЕДИЦИНСКИЙ КОЛЛЕДЖ"
    ),
    MedicalOrganisation(
        mo_code=50010, mo_name=r"ГБПОУ САМАРСКИЙ МЕДИЦИНСКИЙ КОЛЛЕДЖ ИМ.Н.ЛЯПИНОЙ"
    ),
    MedicalOrganisation(mo_code=63023, mo_name=r'ФИЛИАЛ АО "МАКС-М" В Г. САМАРЕ'),
    MedicalOrganisation(
        mo_code=63035, mo_name=r'АО "АСТРАМЕД-МС" (СТРАХОВАЯ МЕДИЦИНСКАЯ КОМПАНИЯ)'
    ),
]


async def set_preset_data():
    async with async_session() as session:
        if await session.get(User, 1):
            return

        session.add_all(mo_list)

        await session.commit()

        medical_organisation_id_miac = (
            (
                await session.execute(
                    select(MedicalOrganisation.id).where(
                        MedicalOrganisation.mo_code == 6005
                    )
                )
            )
            .scalars()
            .first()
        )

        session.add(
            User(
                username="admin",
                password=pwd_context.hash(admin_password),
                full_name="admin",
                phone_number="+79999999999",
                role=UserRole.admin,
                medical_organisation_id=medical_organisation_id_miac,
            )
        )

        await session.commit()
