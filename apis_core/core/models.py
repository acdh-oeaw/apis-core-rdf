from django.db import models

from apis_core.utils import DateParser


# This is abstract class provides a Mixin for APIS models that need
# a temporal component. It provides commonly used felds for start
# and end dates, reps. start and end durations.
class LegacyDateMixin(models.Model):
    start_date = models.DateField(blank=True, null=True, editable=False)
    start_start_date = models.DateField(blank=True, null=True, editable=False)
    start_end_date = models.DateField(blank=True, null=True, editable=False)
    end_date = models.DateField(blank=True, null=True, editable=False)
    end_start_date = models.DateField(blank=True, null=True, editable=False)
    end_end_date = models.DateField(blank=True, null=True, editable=False)
    start_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Start",
    )
    end_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="End",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        skip_date_parsing = getattr(self, "skip_date_parsing", False)
        if not skip_date_parsing:
            start = None
            start_start = None
            start_end = None
            end = None
            end_start = None
            end_end = None

            if self.start_date_written:
                start, start_start, start_end = DateParser.parse_date(
                    self.start_date_written
                )
                # DateParser returns datetime, but we want dates without time
                if start:
                    start = start.date()
                if start_start:
                    start_start = start_start.date()
                if start_end:
                    start_end = start_end.date()

            if self.end_date_written:
                end, end_start, end_end = DateParser.parse_date(self.end_date_written)
                # DateParser returns datetime, but we want dates without time
                if end:
                    end = end.date()
                if end_start:
                    end_start = end_start.date()
                if end_end:
                    end_end = end_end.date()

            self.start_date = start
            self.start_start_date = start_start
            self.start_end_date = start_end
            self.end_date = end
            self.end_start_date = end_start
            self.end_end_date = end_end

        super().save(*args, **kwargs)

        return self
