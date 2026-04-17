from django.db import models
import uuid

class Employee(models.Model):
    
    ROLE_CHOICES = [
        ('Mason', 'Mason'),
        ('Labor', 'Labor'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Labor')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.role})"