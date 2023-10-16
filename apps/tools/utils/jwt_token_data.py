from apps.administration.models import Category, Catalog, Service


def categories(user_type):
    interested_subservice = user_type.subservice.values('id', 'name_uz', 'name_ru', 'name_en')
    interested_subcatalog = user_type.subcatalog.values('id', 'name_uz', 'name_ru', 'name_en')
    interested_subcategory = user_type.subcategory.values('id', 'name_uz', 'name_ru', 'name_en')
    category_ids = list(user_type.subcategory.values_list('category', flat=True).distinct())
    category_data = Category.objects.filter(id__in=category_ids).values('id', 'name_uz',
                                                                        'name_ru', 'name_en')
    for category in category_data:
        sub_categories = interested_subcategory.filter(category=category.get('id'))
        category['subcategory'] = list(sub_categories)

    catalog_ids = list(user_type.subcatalog.values_list('catalog', flat=True).distinct())
    catalog_data = Catalog.objects.filter(id__in=catalog_ids).values('id', 'name_uz',
                                                                     'name_ru', 'name_en')
    for catalog in catalog_data:
        sub_catalogs = interested_subcatalog.filter(catalog=catalog.get('id'))
        catalog['subcatalog'] = list(sub_catalogs)

    service_ids = list(user_type.subservice.values_list('service', flat=True).distinct())
    service_data = Service.objects.filter(id__in=service_ids).values('id', 'name_uz',
                                                                     'name_ru', 'name_en')
    for service in service_data:
        sub_services = interested_subservice.filter(service=service.get('id'))
        service['subservice'] = list(sub_services)
    return {
        "category_data": list(category_data),
        "catalog_data": list(catalog_data),
        "service_data": list(service_data),
    }
