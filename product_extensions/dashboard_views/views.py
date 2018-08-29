from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from saleor.core.utils import get_paginator_items
from saleor.dashboard.views import staff_member_required
from .filters import ProductExtensionFilter
from .forms import ProductExtensionForm

from ..models import ProductExtension


@staff_member_required
@permission_required('product_extensions.view')
def product_extension_list(request):
    product_extensions = (
        ProductExtension.objects.all().select_related('product')
        .order_by('product'))
    product_extension_filter = ProductExtensionFilter(
        request.GET, queryset=product_extensions)
    product_extensions = get_paginator_items(
        product_extensions, settings.DASHBOARD_PAGINATE_BY, request.GET.get('page'))
    # Call this so that cleaned_data exists on the filter_set
    product_extension_filter.form.is_valid()
    ctx = {
        'product_extensions': product_extensions, 'filter_set': product_extension_filter,
        'is_empty': not product_extension_filter.queryset.exists()}
    return TemplateResponse(request, 'product_extensions/dashboard/list.html', ctx)


@staff_member_required
@permission_required('product_extensions.edit')
def product_extension_create(request):
    product_extension = ProductExtension()
    form = ProductExtensionForm(request.POST or None)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy('Dashboard message', 'Created product extension')
        messages.success(request, msg)
        return redirect('product-extension-dashboard-list')
    ctx = {'product_extension': product_extension, 'form': form}
    return TemplateResponse(request, 'product_extensions/dashboard/detail.html', ctx)


@staff_member_required
@permission_required('product_extensions.edit')
def product_extension_details(request, pk):
    product_extension = ProductExtension.objects.get(pk=pk)
    form = ProductExtensionForm(
        request.POST or None, instance=product_extension)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Updated product extension %s') % product_extension.name
        messages.success(request, msg)
        return redirect('product-extension-dashboard-list')
    ctx = {'product_extension': product_extension, 'form': form}
    return TemplateResponse(request, 'product_extensions/dashboard/detail.html', ctx)


@staff_member_required
@permission_required('product_extensions.edit')
def product_extension_delete(request, pk):
    product_extension = get_object_or_404(ProductExtension, pk=pk)
    if request.method == 'POST':
        product_extension.delete()
        msg = pgettext_lazy('Dashboard message',
                            'Removed product extension %s') % product_extension
        messages.success(request, msg)
        return redirect('product-extension-dashboard-list')
    return TemplateResponse(
        request, 'product_extensions/dashboard/modal/confirm_delete.html', {'product_extension': product_extension})
