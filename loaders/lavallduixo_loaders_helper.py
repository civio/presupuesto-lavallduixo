# -*- coding: UTF-8 -*-

def get_programme_id(fc_code, year):
    fc_code = fc_code.ljust(5, '0')  # Fill with zeroes on the right if needed

    # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
    # mapping to be constant over time, we are forced to amend budget data prior to 2015.
    # See https://github.com/dcabo/presupuestos-aragon/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
    programme_mapping = {
        '1340': '1360',     # Prevención de incendios
        '1530': '1521',     # Vivienda
        '1540': '1533',     # Vías públicas
        '1550': '1533',     # Vías públicas
        '1620': '1621',     # Recogida de residuos
        '2300': '2310',     # Acción social
        '2311': '2310',     # Acción social
        '2331': '2310',     # Acción social
        '2332': '2310',     # Acción social
        '2336': '2310',     # Acción social
        '2339': '2310',     # Acción social
        '2399': '2310',     # Acción social
        '2312': '2310',     # Acción social
        '2313': '2310',     # Acción social
        '2321': '2310',
        '2322': '2310',
        '2324': '2310',
        '2330': '2310',
        '2411': '2410',     # Fomento del empleo
        '2412': '2410',     # Fomento del empleo
        '2414': '2410',     # Fomento del empleo
        '2415': '2410',     # Fomento del empleo
        '3231': '3200',     # Educación
        '3320': '3321',     # Bibliotecas y archivos
        '4310': '4300',     # Comercio
        '9240': '9241',     # Participación ciudadana
        '9241': '9242',     # Juventud
    }

    # In 2015 we have to amend some subprogramme codes for a couple of policies with
    # a big number of children.
    programme_mapping_after_2015 = {
        '23109': '2335',    # Hogar Sagrada Familia
        '23110': '2337',    # CRIS
        '23111': '2310',    # Acción social
        '23112': '2310',    # Acción social
        '23113': '2310',    # Acción social
        '23114': '2310',    # Acción social
        '23115': '2310',    # Acción social
        '23116': '2310',    # Acción social
        '23117': '2310',    # Acción social
        '23118': '2310',    # Acción social
        '23119': '2310',    # Acción social
        '23120': '2310',    # Acción social
        '23121': '2310',    # Acción social
        '23122': '2310',    # Acción social
        '23123': '2310',    # Acción social
        '23124': '2310',    # Acción social
        '23125': '2310',    # Acción social
        '23126': '2310',    # Acción social
        '23127': '2310',    # Acción social
        '23128': '2310',    # Acción social
        '31400': '3130',    # Sanitat i consum (only in payments)
    }

    if year < 2015:
        return programme_mapping.get(fc_code[:4], fc_code)
    else:
        return programme_mapping_after_2015.get(fc_code, fc_code)
