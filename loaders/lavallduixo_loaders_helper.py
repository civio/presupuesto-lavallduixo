# -*- coding: UTF-8 -*-

def get_programme_id(fc_code, year):
    fc_code = fc_code.ljust(5, '0')  # Fill with zeroes on the right if needed

    # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
    # mapping to be constant over time, we are forced to amend budget data prior to 2015.
    # See https://github.com/dcabo/presupuestos-aragon/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
    programme_mapping = {
        '13400': '1360',     # Prevención de incendios
        '15300': '1521',     # Vivienda
        '15400': '1533',     # Vías públicas
        '15500': '1533',     # Vías públicas
        '16200': '1621',     # Recogida de residuos
        '23000': '2310',     # Acción social
        '23110': '2310',     # Acción social
        '23120': '2310',     # Acción social
        '23121': '2312',     # Prestaciones económicas individuales (PEI)
        '23124': '2313',     # Renta garantizada
        '23130': '2310',     # Acción social
        '23136': '2314',     # Ayuda a domicilio
        '23210': '2310',
        '23211': '2310',
        '23212': '2310',
        '23213': '2315',     # Universidad popular
        '23215': '2310',     # Acción social
        '23216': '2310',     # Acción social
        '23218': '2310',     # Acción social
        '23221': '2310',
        '23222': '2310',
        '23223': '2310',
        '23224': '2310',
        '23225': '2318',     # Inmigración
        '23226': '2310',
        '23227': '2310',
        '23228': '2310',
        '23229': '2310',
        '23240': '2310',
        '23300': '2310',
        '23310': '2310',     # Acción social
        '23320': '2310',     # Acción social
        '23360': '2310',     # Acción social
        '23390': '2310',     # Acción social
        '23990': '2310',     # Acción social
        '24110': '2410',     # Fomento del empleo
        '24120': '2410',     # Fomento del empleo
        '24140': '2410',     # Fomento del empleo
        '24141': '2410',     # Fomento del empleo
        '24151': '2410',     # Fomento del empleo
        '24152': '2410',     # Fomento del empleo
        '24155': '2410',     # Fomento del empleo
        '24156': '2410',     # Fomento del empleo
        '24157': '2410',     # Fomento del empleo
        '24158': '2410',     # Fomento del empleo
        '32310': '3200',     # Educación
        '33200': '3321',     # Bibliotecas y archivos
        '43100': '4300',     # Comercio
        '43101': '4300',     # Comercio
        '43102': '4300',     # Comercio
        '92400': '9241',     # Participación ciudadana
        '92410': '9242',     # Juventud
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
        '23124': '2310',    # Acción social
        '23125': '2310',    # Acción social
        '23126': '2310',    # Acción social
        '23127': '2310',    # Acción social
        '23128': '2310',    # Acción social
        '23224': '2310',    # Acción social
        '31400': '3130',    # Sanitat i consum (only in payments)

        # We've built the site assuming 4-digit codes. Now 5-digits come along and
        # sometimes the fifth digit is relevant. So we map them into codes we make up.
        # We're losing the exact mapping of our URLs with official documents,
        # but we had lost that anyway in previous years, so it's ok.
        '23103': '2314',    # Ayuda a domicilio
        '23105': '2315',    # Universidad popular
        '23108': '2318',    # Inmigración
        '23122': '2312',    # Prestaciones económicas individuales (PEI)
        '23123': '2313',    # Renta garantizada
    }

    # In 2016 we see what looks like a duplicate of an existing programme, so we
    # merge them together. Something similar happened in 2017.
    programme_mapping_2016 = {
        '15500': '1532',    # Otras inversiones
        '16000': '1610',    # Saneamiento y abastecimiento de agua
        '43120': '4300',    # Comercio
        '24120': '2411',    # Fomento del empleo
        '24121': '2411',    # Fomento del empleo
        '24122': '2411',    # Fomento del empleo
    }
    if year in [2016, 2017]:
        fc_code = programme_mapping_2016.get(fc_code, fc_code)

    # Do the overall mapping
    if year < 2015:
        return programme_mapping.get(fc_code, fc_code)
    else:
        return programme_mapping_after_2015.get(fc_code, fc_code)
