from django.contrib import admin

from solo.admin import SingletonModelAdmin

from apps.main.models import MainBanner, Product, Category, AboutUs, \
    SliderAboutUsOne, SliderAboutUsTwo, SliderAboutUsThree, Contact, Schedule, \
    Delivery


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    list_display = ('image',)

    def has_add_permission(self, request):
        return self.model.objects.count() < 1


@admin.register(Category)
class CategoryInline(admin.ModelAdmin):
    list_display = ('name',)

    def has_add_permission(self, request):
        return self.model.objects.count() < 6


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_available', 'is_populate', 'category')
    fieldsets = [
        [None, {
            'fields': [
                'title', 'description',
                ('category', 'is_available', 'is_populate', 'image',),
            ]
        }],
        [('Порции'), {
            'fields': [
                ('portion', 'price'), ('portion_two', 'price_two')
            ]
        }]
    ]


@admin.register(AboutUs)
class AboutUsAdmin(SingletonModelAdmin):
    pass


@admin.register(SliderAboutUsOne)
class AboutUsAdmin(admin.ModelAdmin):
    pass


@admin.register(SliderAboutUsTwo)
class AboutUsAdmin(admin.ModelAdmin):
    pass


@admin.register(SliderAboutUsThree)
class AboutUsAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class AboutUsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return self.model.objects.count() < 2


@admin.register(Schedule)
class AboutUsAdmin(admin.ModelAdmin):
    pass


@admin.register(Delivery)
class AboutUsAdmin(admin.ModelAdmin):
    pass

