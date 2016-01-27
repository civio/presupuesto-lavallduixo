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
            # '1533': '1530',     # Vías públicas
        }

        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            fc_code = self.clean(line[2]).ljust(4,'0')  # Fill with zeroes on the right if needed

            # For years before 2015 we check whether we need to amend the programme code
            year = re.search('municipio/(\d+)/', filename).group(1)
            if year in ['2011', '2012', '2013', '2014']:
                new_programme = programme_mapping.get(fc_code)
                if new_programme:
                    fc_code = new_programme

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
