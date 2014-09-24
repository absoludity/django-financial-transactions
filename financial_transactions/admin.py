from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from financial_transactions.models import (
    Account,
    Transaction,
    TransactionCategoryHint,
)


class UncategorisedListFilter(SimpleListFilter):
    title = _('categories')
    parameter_name = 'categories'

    def lookups(self, request, model_admin):
        return (
            ('uncategorised', _('Uncategorised')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'uncategorised':
            return queryset.filter(category=None)
        return queryset


class TransactionAdmin(admin.ModelAdmin):
    # XXX Including category puts a massive load on the list view,
    # even if you're only displaying category.id - it seems to be doing
    # a lot more work that just retrieving the FK.
    list_display = ('date', 'account', 'amount', 'category', 'tid', 'memo')
    ordering = ('-date',)
    list_filter = ('account', UncategorisedListFilter)


class TransactionCategoryHintAdmin(admin.ModelAdmin):
    list_display = ('category', 'memo_like')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_id')


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionCategoryHint, TransactionCategoryHintAdmin)
