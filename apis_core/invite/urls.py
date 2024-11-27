from django.urls import path

from apis_core.invite.views import Invite

urlpatterns = [
    path("invite/<uuid:invite>", Invite.as_view()),
]
