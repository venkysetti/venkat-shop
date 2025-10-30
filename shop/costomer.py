from django.db import models

class  Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)

    def isexits(self):
            return Customer.objects.filter(mobile=self.mobile).exists() or Customer.objects.filter(email=self.email).exists()
    @staticmethod
    def get_email(email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None