from django.contrib import admin

from .models import TagAssociation
from .app_settings import mumble_active

class TagAssociationAdmin(admin.ModelAdmin):
    list_display = ['tag', 'enabled', '_groups']

    def _list_2_html_w_tooltips(self, my_items: list, max_items: int) -> str:    
        """converts list of strings into HTML with cutoff and tooltip"""
        items_truncated_str = ', '.join(my_items[:max_items])
        if not my_items:
            result = None
        elif len(my_items) <= max_items:
            result = items_truncated_str
        else:
            items_truncated_str += ', (...)'
            items_all_str = ', '.join(my_items)
            result = format_html(
                '<span data-tooltip="{}" class="tooltip">{}</span>',
                items_all_str,
                items_truncated_str
            )
        return result

    def _groups(self, obj):
        my_groups = [x.name for x in obj.groups.order_by('name')]
        
        return self._list_2_html_w_tooltips(
            my_groups, 
            10
        )
       
    _groups.short_description = 'groups'


admin.site.register(TagAssociation, TagAssociationAdmin)