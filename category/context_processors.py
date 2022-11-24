from .models import Category, Age, Charector, Brand

def menu_links(request):
    links = Category.objects.exclude(parent__isnull=False)
    age_link = Age.objects.all()
    charector_link = Charector.objects.all()
    brand_link = Brand.objects.all()
    context = {
        'links' : links,
        'age_link' : age_link,
        'charector_link' : charector_link,
        'brand_link': brand_link
    }
    return context