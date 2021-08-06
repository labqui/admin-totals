# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList


class ChangeListTotals(ChangeList):
    def get_results(self, *args, **kwargs):
        super(ChangeListTotals, self).get_results(*args, **kwargs)
        if hasattr(self.model_admin, 'list_totals'):
            self.aggregations = []

            list_totals = {}
            list_totals_format = {}
            for field, fun1, fun_format in self.model_admin.list_totals:
                list_totals[field] = fun1
                list_totals_format[field] = fun_format

            for field in self.list_display:
                if field in list_totals:
                    self.aggregations.append(
                        self.result_list.aggregate(agg=list_totals_format[field](list_totals[field](field)))['agg'])
                else:
                    self.aggregations.append('')


class ModelAdminTotals(admin.ModelAdmin):
    change_list_template = 'admin_totals/change_list_totals.html'

    def get_changelist(self, request, **kwargs):
        return ChangeListTotals
