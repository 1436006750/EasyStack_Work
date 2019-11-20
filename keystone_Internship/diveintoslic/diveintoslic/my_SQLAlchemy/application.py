# -*- coding: utf-8 -*-

from model import Test
import api


def query_all_in_test_table():
    db_api = api.API()
    rv, date = db_api.get_all_content(Test)
    print date










