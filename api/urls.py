from django.urls import path
from . import views

urlpatterns = [
    path("instructor", views.InstructorList.as_view()),
    path("checkin", views.CheckInList.as_view()),
    path("checkin/<int:id>", views.CheckInListByInstructor.as_view()),
    path("checkout", views.CheckOutList.as_view()),
    path("checkout/<int:id>", views.CheckOutListByInstructor.as_view()),
    path("summary/<str:month>", views.MonthlySummary.as_view()),
]
