# -*- coding: utf-8 -*-
# Copyright (c) 2018 SLIC personal studio.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from diveintoslic import exception
from diveintoslic.job1.wsgi import Application
# from mysql_function import MySql
from mysql_sqlalchemy import *


# USER1 = {
#     "id": uuid.uuid4().hex,
#     "name": uuid.uuid4().hex
# }
#
# USER2 = {
#     "id": uuid.uuid4().hex,
#     "name": uuid.uuid4().hex
# }
#
# USERS = [USER1, USER2]

# Example = MySql()   # 实例化一个数据库使用对象

Operator = Sql_Operation()  # 实例化一个sqlalchmey数据库操作对象


class Users(Application):
    def get_user(self, request, user_name):
        result = Operator.orm_query_by_name(user_name)
        return result

    def list_users(self, request):
        # import pdb
        # pdb.set_trace()
        result = Operator.orm_query_all()
        return result

    def create_user(self, request, user_name, user_id):
        result = Operator.orm_insert(user_name, user_id)
        return result

    def delete_user(self, request, user_name):
        # import pdb; pdb.set_trace()
        result = Operator.orm_delete_by_name(user_name)
        return result

    def update_user(self, request, user_name, new_name, new_id):
        result = Operator.orm_change_by_name(user_name, new_name, new_id)
        return result





# class Users(Application):
#     def get_user(self, request, user_name):
#         result = Example.lookup_one_my_sql(user_name)
#         return result
#
#     def list_users(self, request):
#         result = Example.lookup_all_my_sql()
#         return result
#
#     def create_user(self, request, user_name):
#         # 如果查询到的记录为 0, 则开始创建记录， 否则返回已有该记录
#         record = Example.query_Record_name(user_name)
#         if record == 1:
#             sentence_back = ("姓名为 %s 的人已经存在，请重新选择！" %user_name)
#
#             return sentence_back
#
#         else:
#             print("姓名为%s的人不存在，正在生成！" % user_name)
#             user_id = uuid.uuid4().hex
#             result = Example.add_my_sql(user_name, user_id)
#             if result == 1:
#                 sentence_back = ("姓名为 %s 的人的记录添加成功!" %user_name)
#
#             else:
#                 sentence_back = ("姓名为 %s 的人的记录添加失败功!" %user_name)
#
#         return sentence_back
#
#     def delete_user(self, request, user_name):
#         recode = Example.query_Record_name(user_name)
#         if recode == 1:
#             sentence_back = Example.delete_my_sql_name(user_name)
#         else:
#             sentence_back = ("%s 这条记录没有查询到，请确定您的输入无误！" %user_name)
#
#         return sentence_back
#
#     def update_user(self, request, user_name, new_name, new_id):
#         recode = Example.query_Record_name(user_name)
#         if recode == 1:
#             # 有这个人，可以进行下一步---更新操作
#             sentence_back = Example.update_user_by_name(user_name, new_name, new_id)
#         else:
#             sentence_back = ("%s 这条记录尚未记录在数据库中, 请确认您的用户姓名是否正确" % user_name)
#
#         return sentence_back
