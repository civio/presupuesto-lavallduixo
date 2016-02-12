# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *
import csv
import os
import re

class LavallduixoBudgetLoader(SimpleBudgetLoader):

    # An artifact of the in2csv conversion of the original XLS files is a trailing '.0', which we remove here
    def clean(self, s):
        return s.split('.')[0]

    def parse_item(self, filename, line):
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
        }

        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            fc_code = self.clean(line[2]).ljust(5, '0')  # Fill with zeroes on the right if needed

            # We check whether we need to amend the programme code
            year = re.search('municipio/(\d+)/', filename).group(1)
            if int(year) < 2015:
                fc_code = programme_mapping.get(fc_code[:4], fc_code)
            else:
                fc_code = programme_mapping_after_2015.get(fc_code, fc_code)


            return {
                'is_expense': True,
                'is_actual': is_actual,
                'fc_code': fc_code[:4],
                'ec_code': self.clean(line[3])[:3],
                'ic_code': '100',
                'item_number': self.clean(line[3])[-2:],    # Last two digits
                'description': line[0],
                'amount': self._parse_amount(line[7 if is_actual else 4])
            }

        else:
            return {
                'is_expense': False,
                'is_actual': is_actual,
                'ec_code': self.clean(line[1])[:3],
                'ic_code': '100',                           # All income goes to the root node
                'item_number': self.clean(line[1])[-2:],    # Last two digits
                'description': line[2],
                'amount': self._parse_amount(line[6 if is_actual else 3])
            }

    # We don't have an institutional breakdown in Torrelodones, so we create just a catch-all organism.
    # (We then configure the theme so we don't show an institutional breakdown anywhere.)
    def load_institutional_classification(self, path, budget):
        InstitutionalCategory(  institution='1',
                                section='10',
                                department='100',
                                description="Ayuntamiento de La Vall d'Uixó",
                                budget=budget).save()
