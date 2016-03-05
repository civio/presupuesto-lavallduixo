# -*- coding: UTF-8 -*-

import datetime

from budget_app.loaders import PaymentsLoader
from budget_app.models import Budget
from lavallduixo_loaders_helper import *

class LavallduixoPaymentsLoader(PaymentsLoader):

    # Parse an input line into fields
    def parse_item(self, budget, line):
        # The date is not always available
        try:
            date=datetime.datetime.strptime(line[7], "%Y-%m-%d")
        except ValueError:
            date=None

        # The item id is of the form 2013/N/170/132/214/, with the following fields:
        # Year, ?, ?, programme, economic concept.
        item_fields = line[1].split('/')

        # The programme id needs to be mapped, because of changing legislation.
        # But beware, some items are payed the year after, so we need to pick the right year
        # from the payment description, not from the budget itself.
        programme_id = get_programme_id(item_fields[3].ljust(5, '0'), int(item_fields[0]))[:4]

        # But what we want as area is the programme description
        programme = Budget.objects.get_all_descriptions(budget.entity)['functional'][programme_id]

        return {
            'area': programme,
            'fc_code': programme_id,
            'ec_code': item_fields[4],
            'date': date,
            'contract_type': '',
            'payee': self._titlecase(line[3].strip()),
            'description': self._spanish_titlecase(line[2].strip()),
            'amount': self._read_english_number(line[5])
        }
