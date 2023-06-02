import django_tables2 as tables
from django.utils.safestring import mark_safe


input_form = """
  <input type="checkbox" name="keep" value="{}" title="keep this"/> |
  <input type="checkbox" name="remove" value="{}" title="remove this"/>
"""

class MergeColumn(tables.Column):
    """renders a column with to checkbox - used to select objects for merging"""

    def __init__(self, *args, **kwargs):
        super(MergeColumn, self).__init__(*args, **kwargs)

    def render(self, value):
        return mark_safe(input_form.format(value, value))


