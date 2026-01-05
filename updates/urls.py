from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('login/', login_view),
    path('logout/', logout_view),
    path('add/', add_announcement),
    path('manage/', manage_announcements),
    path('delete/<int:announcement_id>/', delete_announcement),
    path('register-staff/', register_staff),
    path('deactivate-staff/<int:user_id>/', deactivate_staff),
    path('delete-staff/<int:user_id>/', delete_staff),
    path('staff/', staff_list),
    path('staff/', staff_list),
    path('reactivate-staff/<int:user_id>/', reactivate_staff),
]