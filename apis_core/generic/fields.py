from datetime import date
import re
from typing import Callable, List, Optional, Tuple
from django.db.models import DateTimeField, CharField
from django.forms import DateField, ValidationError

from apis_core.history.models import APISHistoryTableBase


class StringDateTimeField(CharField):
    """A simple CharField, that populates datetime fields with its own value"""

    def pre_save(self, model_instance, add):
        name = self.attname.removesuffix("_string")
        value = getattr(model_instance, self.attname)
        if hasattr(model_instance, f"{name}_datetime"):
            setattr(model_instance, f"{name}_datetime", value)
        if hasattr(model_instance, f"{name}_datetime_from"):
            setattr(model_instance, f"{name}_datetime_from", value)
        if hasattr(model_instance, f"{name}_datetime_to"):
            setattr(model_instance, f"{name}_datetime_to", value)
        return super().pre_save(model_instance, add)


class DateTimeIntervalCharField:
    def contribute_to_class(self, cls, name):
        StringDateTimeField(max_length=255, blank=True, null=True).contribute_to_class(
            cls, f"{name}_string"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime_from"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime_to"
        )


class FuzzyDateField(CharField):
    def __init__(
        self,
        parser: Optional[Callable[[str], Tuple[date, date, date]]] = None,
        regex_patterns: Optional[List[Tuple[str, str, str]]] = [
            (
                r"(?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})",
                r"(?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})",
                r"(?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})",
            )
        ],
        *args,
        **kwargs,
    ):
        if parser and regex_patterns:
            raise ValueError(
                "Specify either a parser function or regex patterns, not both."
            )
        self.parser = parser
        self.regex_patterns = regex_patterns
        super().__init__(*args, **kwargs)

    def _parse_date_using_regex_match(self, regex_match: re.Match) -> date:
        match_dict = regex_match.groupdict()
        if (
            "year" not in match_dict
            or "month" not in match_dict
            or "day" not in match_dict
        ):
            raise ValueError(
                f"Regex pattern does not contain all needed named groups (year, month, day): {regex_match}"
            )
        ret_date = f"{match_dict['year']}-{match_dict['month'] if match_dict['month'] is not None else '01'}-{match_dict['day'] if match_dict['day'] is not None else '01'}"

        return ret_date

    def _parse_date_using_list_of_regexes(self, value: str):
        for (
            date_sort_pattern,
            date_from_pattern,
            date_to_pattern,
        ) in self.regex_patterns:
            date_sort = re.search(date_sort_pattern, value)
            date_from = re.search(date_from_pattern, value)
            date_to = re.search(date_to_pattern, value)
            if date_sort and date_from and date_to:
                return (
                    self._parse_date_using_regex_match(date_sort),
                    self._parse_date_using_regex_match(date_from),
                    self._parse_date_using_regex_match(date_to),
                )
        return None, None, None

    def pre_save(self, model_instance, add):
        name = self.attname
        value = getattr(model_instance, name)
        if self.parser:
            try:
                date, date_from, date_to = self.parser(value)
                setattr(model_instance, f"{name}_date_sort", date)
                setattr(model_instance, f"{name}_date_from", date_from)
                setattr(model_instance, f"{name}_date_to", date_to)
            except Exception as e:
                raise ValidationError(f"Error parsing date string: {e}")
        elif self.regex_patterns:
            try:
                date_sort, date_from, date_to = self._parse_date_using_list_of_regexes(
                    value
                )
                setattr(model_instance, f"{name}_date_sort", date_sort)
                setattr(model_instance, f"{name}_date_from", date_from)
                setattr(model_instance, f"{name}_date_to", date_to)
            except Exception as e:
                raise ValidationError(f"Error parsing date string with regex: {e}")
        return value

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        if not issubclass(cls, APISHistoryTableBase):
            DateField(editable=False, blank=True, null=True).contribute_to_class(
                cls, f"{name}_date_sort"
            )
            DateField(editable=False, blank=True, null=True).contribute_to_class(
                cls, f"{name}_date_from"
            )
            DateField(editable=False, blank=True, null=True).contribute_to_class(
                cls, f"{name}_date_to"
            )
            setattr(cls, name, self)

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     if self.parser:
    #         kwargs["parser"] = self.parser
    #         if "regex_patterns" in kwargs:
    #             del kwargs["regex_patterns"]
    #     if self.regex_patterns:
    #         kwargs["regex_patterns"] = self.regex_patterns

    #     return name, path, args, kwargs
