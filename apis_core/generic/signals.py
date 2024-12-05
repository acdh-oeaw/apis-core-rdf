from django.db.models.signals import ModelSignal

pre_merge_with = ModelSignal(use_caching=True)
post_merge_with = ModelSignal(use_caching=True)
