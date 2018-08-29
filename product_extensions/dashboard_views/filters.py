from django.utils.translation import npgettext, pgettext_lazy
from django_filters import (CharFilter, OrderingFilter)

from saleor.core.filters import SortedFilterSet

from ..models import ProductExtension

SORT_BY_FIELDS = {
    'product__name': pgettext_lazy('Product list sorting option', 'name')}


class ProductExtensionFilter(SortedFilterSet):
    product__name = CharFilter(
        label=pgettext_lazy('Product list filter label', 'Name'),
        lookup_expr='icontains')
    sort_by = OrderingFilter(
        label=pgettext_lazy('Product list filter label', 'Sort by'),
        fields=SORT_BY_FIELDS.keys(),
        field_labels=SORT_BY_FIELDS)

    class Meta:
        model = ProductExtension
        fields = []

    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            'Number of matching records in the dashboard product extensions list',
            'Found %(counter)d matching product extension',
            'Found %(counter)d matching product extensions',
            number=counter) % {'counter': counter}
