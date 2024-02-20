from django.db import models


# Create your models here.
class Instructor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class CheckIn(models.Model):
    time = models.TimeField()
    date = models.DateField()
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)


class CheckOut(models.Model):
    time = models.TimeField()
    date = models.DateField()
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)

