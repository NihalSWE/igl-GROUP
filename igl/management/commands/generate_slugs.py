from django.core.management.base import BaseCommand
from django.utils.text import slugify
from igl.models import NavMenu

class Command(BaseCommand):
    help = 'Generate slugs for all existing NavMenu items'

    def handle(self, *args, **kwargs):
        # Loop through all the NavMenu objects
        for menu in NavMenu.objects.all():
            if not menu.slug_name:
                # Generate the slug_name
                slug_base = slugify(menu.name)
                slug = slug_base
                num = 1
                while NavMenu.objects.filter(slug_name=slug).exists():
                    slug = f"{slug_base}-{num}"
                    num += 1
                # Save the generated slug_name
                menu.slug_name = slug
                menu.save()

        self.stdout.write(self.style.SUCCESS('Slug names generated successfully for all NavMenu items.'))