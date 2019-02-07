from django import forms
from django.db.models import Q
from django.utils.translation import pgettext_lazy
from django.urls import reverse_lazy


from saleor.product.models import Product
from saleor.dashboard.product.forms import RichTextField
from saleor.dashboard.forms import AjaxSelect2ChoiceField
from ..models import ProductExtension


class ProductExtensionForm(forms.ModelForm):
    product = AjaxSelect2ChoiceField(
        queryset=Product.objects.all(),
        fetch_data_url=reverse_lazy('dashboard:ajax-products'))

    class Meta:
        model = ProductExtension
        verbose_name_plural = 'extension products'
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ProductExtensionForm, self).__init__(*args, **kwargs)

        # Modify the queryset so that we don't show products that are
        # already extension.
        # We need to do this differently for when the
        # user is adding vs editing so we can explicitly include the current
        # product when they are editing.
        if self.instance.pk:
            self.fields['product'].queryset = self.fields[
                'product'].queryset.filter(
                    Q(id=self.instance.product.pk) |
                    Q(extension__isnull=True))
        else:
            self.fields['product'].queryset = self.fields[
                'product'].queryset.filter(extension__isnull=True)

        if self.instance.product:
            self.fields['product'].set_initial(self.instance.product)
