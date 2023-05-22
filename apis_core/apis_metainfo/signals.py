from django.db.models.signals import ModelSignal

pre_duplicate = ModelSignal(use_caching=True)
post_duplicate = ModelSignal(use_caching=True)
