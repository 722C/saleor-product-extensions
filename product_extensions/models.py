from django.db import models

from django.utils.translation import pgettext_lazy

from saleor.core.permissions import MODELS_PERMISSIONS


# Add in the permissions specific to our models.
MODELS_PERMISSIONS += [
    'product_extensions.view',
    'product_extensions.edit'
]


class ProductExtension(models.Model):
    product = models.OneToOneField(
        'product.Product', on_delete=models.CASCADE, related_name='extension')
    new = models.BooleanField(default=False)
    top_seller = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'product_extensions'

        permissions = (
            ('view', pgettext_lazy('Permission description',
                                   'Can view product extensions')
             ),
            ('edit', pgettext_lazy('Permission description',
                                   'Can edit product extensions')))

    def __str__(self):
        return self.product.name
