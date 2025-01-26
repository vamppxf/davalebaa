from django.core.management.base import BaseCommand
from django.db.models import Count, Max, Min, Avg, Sum
from shop.models import Category, Item

class Command(BaseCommand):
    help = "Analyze store data"

    def handle(self, *args, **kwargs):
        category = Category.objects.first()
        if category:
            item_count = Item.objects.filter(category=category).count()
            self.stdout.write(f"Category '{category.name}' has {item_count} items.")

        prices = Item.objects.aggregate(
            max_price=Max('price'),
            min_price=Min('price'),
            avg_price=Avg('price')
        )
        self.stdout.write(f"Max price: {prices['max_price']}, Min price: {prices['min_price']}, Avg price: {prices['avg_price']}")

        categories = Category.objects.annotate(
            items_count=Count('item'),
            total_price=Sum('item__price')
        )
        for cat in categories:
            self.stdout.write(f"Category '{cat.name}': Items Count = {cat.items_count}, Total Price = {cat.total_price}")

        items = Item.objects.select_related('category')
        for item in items:
            self.stdout.write(f"Item '{item.name}' belongs to Category '{item.category.name}'")

        items_with_tags = Item.objects.prefetch_related('tags')
        for item in items_with_tags:
            tags = ", ".join(tag.name for tag in item.tags.all())
            self.stdout.write(f"Item '{item.name}' has Tags: {tags}")
