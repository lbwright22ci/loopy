from django.db import models

# Create your models here.
class Contact(models.Model):
    """"
    Stores contact equiries from customers and potential customers

    Fields in this model are `name`, `email`, `subject`, 
    `message`, `created_on`, `read`
    """
    SUB_OPTIONS =( (0, "A question about a product"), (1, "A question about my order"), (2, "Other"))
    
    name = models.CharField(max_length=80, blank = False)
    email = models.EmailField(blank = False) 
    subject = models.IntegerField(choices=SUB_OPTIONS, default=2)
    message = models.CharField(max_length = 500, blank = False )
    created_on = models.DateTimeField(auto_now = True )
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Customer contact messages"
        verbose_name = "Customer contact message"

    def __str__(self):
        return f"Message from {self.name}, about {self.get_subject_display()}. Read = {self.read} Date = {self.created_on}"
