import re
from datetime import date
from typing import Callable, Tuple

from django.db.models import CharField, DateField
from django.forms import ValidationError

from apis_core.history.models import APISHistoryTableBase
from apis_core.utils import DateParser


class GenericDateIntervalField(CharField):
    """Add additional fields to the model containing this field
    The check using `hasattr` and `setattr` to check the existence
    of the field is taken from https://github.com/django-money/django-money/blob/main/djmoney/models/fields.py#L255
    Without that the migrations did fail again and again ...
    """

    def add_generated_date_field(self, cls, name):
        date_field = DateField(editable=False, blank=True, null=True)
        cls.add_to_class(name, date_field)
        setattr(self, f"_{name}", date_field)

    def contribute_to_class(self, cls, name):
        for field_name in [f"{name}_date_sort", f"{name}_date_from", f"{name}_date_to"]:
            if not issubclass(cls, APISHistoryTableBase) and not hasattr(
                self, f"_{field_name}"
            ):
                self.add_generated_date_field(cls, field_name)
        super().contribute_to_class(cls, name)
        setattr(cls, name, self)


class FuzzyDateParserField(GenericDateIntervalField):
    def __init__(
        self,
        parser: Callable[[str], Tuple[date, date, date]] = DateParser.parse_date,
        *args,
        **kwargs,
    ):
        self.parser = parser
        super().__init__(*args, **kwargs)

    def _populate_fields(self, model_instance):
        name = self.attname
        value = getattr(model_instance, name)
        if not getattr(model_instance, "skip_date_parsing", False):
            try:
                date_sort, date_from, date_to = self.parser(value)
                setattr(model_instance, f"{name}_date_sort", date_sort)
                setattr(model_instance, f"{name}_date_from", date_from)
                setattr(model_instance, f"{name}_date_to", date_to)
            except Exception as e:
                raise ValidationError(f"Error parsing date string: {e}")

    def pre_save(self, model_instance, add):
        self._populate_fields(model_instance)
        return super().pre_save(model_instance, add)


FROM_PATTERN = r"<from: (?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})>"
TO_PATTERN = r"<to: (?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})>"
SORT_PATTERN = r"<sort: (?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})>"


class FuzzyDateRegexField(FuzzyDateParserField):
    """This Field allows you to define different regexes for
    extracting the `from`, the `to` and the `sort` values from
    the string. So, the string "2024 <sort: 2024-06-31>" could
    be parsed so that the `_date_sort` field is set to
    datetime.date(2024, 6, 1).
    The pattern hat to contain a <year> group, a <month> group and a <day> group.
    """

    def __init__(
        self,
        from_pattern=FROM_PATTERN,
        to_pattern=TO_PATTERN,
        sort_pattern=SORT_PATTERN,
        *args,
        **kwargs,
    ):
        self.from_pattern = from_pattern
        self.to_pattern = to_pattern
        self.sort_pattern = sort_pattern
        super().__init__(*args, **kwargs)

    def _match_to_date(self, regex_match: re.Match) -> date:
        match_dict = regex_match.groupdict()
        print(match_dict.keys())
        if match_dict.keys() >= {"day", "month", "year"}:
            month = match_dict.get("month", "01")
            day = match_dict.get("day", "01")
            return f"{match_dict['year']}-{month}-{day}"
        raise ValueError(
            f"Regex pattern does not contain all needed named groups (year, month, day): {match_dict}"
        )

    def _populate_fields(self, model_instance):
        super()._populate_fields(model_instance)
        name = self.attname
        value = getattr(model_instance, name)
        if match := re.search(self.sort_pattern, value):
            setattr(model_instance, f"{name}_date_sort", self._match_to_date(match))
        if match := re.search(self.from_pattern, value):
            setattr(model_instance, f"{name}_date_from", self._match_to_date(match))
        if match := re.search(self.to_pattern, value):
            setattr(model_instance, f"{name}_date_to", self._match_to_date(match))
