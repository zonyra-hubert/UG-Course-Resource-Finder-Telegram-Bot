from django.db import models

# Create your models here.
class Course(models.Model):
    # e.g., DCIT203
    code = models.CharField(max_length=10, unique=True) 
    
    # e.g., Digital and Logic Systems
    title = models.CharField(max_length=255) 
    
    # e.g., 3
    credits = models.IntegerField() 
    
    # Detailed course description
    description = models.TextField(blank=True) 
    
    # Link to the shared notes/syllabus
    resource_link = models.URLField(blank=True) 
    level = models.CharField(max_length=10, null=True)  # e.g., 200, 300
    semester = models.CharField(max_length=10, null=True)  # e.g., sem1, sem2
    

    def __str__(self):
        return f"{self.code}: {self.title}"

# Run migrations to create the database tabl