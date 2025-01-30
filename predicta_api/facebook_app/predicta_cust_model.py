from django.db import models

class PredictaCustomer(models.Model):
    id = models.IntegerField(primary_key=True)  # Assuming `id` is the primary key in your SQL table
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    cname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    plandet = models.CharField(max_length=255)
    costdet = models.CharField(max_length=255)
    validity = models.DateField(null=True, blank=True)
    address = models.TextField()
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    plantype = models.CharField(max_length=255)
    users = models.IntegerField()
    city = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=20)
    cnameid = models.CharField(max_length=255)
    logourl = models.URLField(max_length=500)
    themetype = models.CharField(max_length=255)
    custome_added = models.DateField(null=True, blank=True)
    auzureid = models.CharField(max_length=255)

    class Meta:
        db_table = 'predicta_customer'  # Specify the actual table name
        managed = False  # Since this table already exists in your database, don't let Django manage it


