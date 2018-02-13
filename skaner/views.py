from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView
from django.views.generic.list import ListView

from .models import Website, WebsiteCategory, WebsitePage
from .tasks import category_count, upload_from_csv, website_detail


class WebsiteListView(View):

    def get(self, request):
        website_list = Website.objects.all().order_by('title')
        website_list2 = Website.objects.all().order_by('category')
        category_list = WebsiteCategory.objects.all()
        ctx = {
            'website_list': website_list,
            'website_list2': website_list2,
            'category_list': category_list,
        }
        return render(request, 'skaner/website_list.html', ctx)

    def post(self, request):
        category_id = request.POST.get('dropdown')
        return redirect('/website_list/%s' % category_id)


class WebsiteListByCategory(View):

    def get(self, request, id):
        website = Website.objects.filter(category=id)
        category_list = WebsiteCategory.objects.all()
        ctx = {
            'website_list': website,
            'category_list': category_list,
        }
        return render(request, 'skaner/website_list.html', ctx)

    def post(self, request, id):
        category_id = request.POST.get('dropdown')
        return redirect('/website_list/%s' % category_id)


class WebsiteListUploadView(View):

    def get(self, request):
        return render(request, 'skaner/website_list_confirm_upload.html')

    def post(self, request):
        upload_from_csv.delay()
        messages.success(self.request, 'We are uploading Website List! Wait a moment and refresh this page')
        return redirect('website_list')


class WebsiteDetailView(View):

    def get(self, request, id):
        website = Website.objects.get(id=id)
        website_page = WebsitePage.objects.filter(website=website)
        ctx = {
            'website': website,
            'website_page_list': website_page,
        }
        return render(request, 'skaner/website_detail_view.html', ctx)

    def post(self, request, id):
        website_detail.delay(id)
        messages.success(self.request, 'We are uploading Website Details! Wait a moment and refresh this page')
        return redirect('/website_detail/%s' % id)


class WebsiteAddView(CreateView):
    model = Website
    fields = [
        'url',
        'category'
    ]
    success_url = '/'


class WebsiteCategoryListView(ListView):
    template_name = 'websitecategory_list.html'
    model = WebsiteCategory

    ordering = ['name']

    def post(self, request):
        category_count.delay()
        messages.success(self.request, "We are updating category's count! Wait a moment and refresh this page")
        return redirect('website_category_list')


class WebsiteCategoryAddView(CreateView):
    model = WebsiteCategory
    fields = [
        'name',
        'description'
    ]
    success_url = '/website_category_list/'


