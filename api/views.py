from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Instructor, CheckIn, CheckOut
from .serializers import (
    InstructorSerializer,
    CheckInSerializer,
    CheckOutSerializer,
    MonthlySummarySerializer,
)
from django.db import connection

# Create your views here.


class InstructorList(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer


class CheckInList(generics.ListCreateAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer

    def perform_create(self, serializer):
        instructor_id = self.request.data.get("instructor_id")
        date = self.request.data.get("date")
        checkin = CheckIn.objects.filter(
            instructor_id=instructor_id, date=date
        ).order_by("-id")

        checkout = CheckOut.objects.filter(
            instructor_id=instructor_id, date=date
        ).order_by("-id")

        if len(checkin) > len(checkout):
            raise ValidationError({"error": "Hasn't checked out "})

        if checkout and (checkout[0].time > serializer.validated_data["time"]):
            raise ValidationError(
                {"error": "Invalid time. Instructor already checked after this time"}
            )

        if checkin and (not checkout or checkin[0].time > checkout[0].time):
            raise ValidationError(
                {"error": "Already checked in. Please checkout to continue"}
            )

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckInListByInstructor(generics.ListAPIView):
    serializer_class = CheckInSerializer

    def get_queryset(self):
        instructor_id = self.kwargs.get("id")
        return CheckIn.objects.filter(instructor_id=instructor_id).order_by("-id")


class CheckOutList(generics.ListCreateAPIView):
    queryset = CheckOut.objects.all()
    serializer_class = CheckOutSerializer

    def perform_create(self, serializer):
        instructor_id = serializer.validated_data["instructor_id"]
        date = self.request.data.get("date")
        has_checked_in = (
            CheckIn.objects.filter(instructor_id=instructor_id, date=date)
            .order_by("-id")
            .first()
        )

        checkout = (
            CheckOut.objects.filter(instructor_id=instructor_id, date=date)
            .order_by("-id")
            .first()
        )

        if checkout and (checkout.time > has_checked_in.time):
            raise ValidationError({"error": "Already checkedout"})

        if not has_checked_in:
            raise ValidationError(
                {"error": "Instructor must check in before checking out."}
            )

        else:
            if serializer.validated_data["time"] <= has_checked_in.time:
                raise ValidationError(
                    {"error": "check out time should be after checkin time"}
                )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckOutListByInstructor(generics.ListAPIView):
    serializer_class = CheckOutSerializer

    def get_queryset(self):
        instructor_id = self.kwargs.get("id")
        return CheckOut.objects.filter(instructor_id=instructor_id).order_by("-id")


class MonthlySummary(generics.ListAPIView):

    serializer_class = MonthlySummarySerializer

    def get_queryset(self):
        month = self.kwargs.get('month')
        if int(month) < 10:
            month = "0" + str(month)
        with connection.cursor() as cursor:
            cursor.execute(
                f""" 
                WITH RankedCheckin AS (
                    SELECT c.*,
                            ROW_NUMBER() OVER (PARTITION BY instructor_id_id ORDER BY date, time) AS rank
                    FROM api_checkin c
                    ), RankedCheckout AS (
                    SELECT co.*,
                            ROW_NUMBER() OVER (PARTITION BY instructor_id_id ORDER BY date, time) AS rank
                    FROM api_checkout co
                    )
                    SELECT i.name as name, STRFTIME('%m', rc.date) as month,
                        SUM(CASE WHEN rc.rank = co.rank THEN strftime('%s', co.time) - strftime('%s', rc.time) END) / 3600.0 AS total_hours
                    FROM api_instructor i
                    INNER JOIN RankedCheckin rc ON rc.instructor_id_id = i.id
                    INNER JOIN RankedCheckout co ON co.instructor_id_id = rc.instructor_id_id
                    WHERE rc.rank = co.rank  AND rc.time < co.time and month = '{month}'
                    GROUP BY month, i.name 
                    ORDER BY month;
                """
            )
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
