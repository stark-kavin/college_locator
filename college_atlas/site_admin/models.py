from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Country(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True) 

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name

class State(TimeStampedModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='states')

    class Meta:
        unique_together = ('name', 'country')
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

class District(TimeStampedModel):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='districts')

    class Meta:
        unique_together = ('name', 'state')
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Degree(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. B.E. Computer Science")
    duration_years = models.PositiveIntegerField(default=4)

    class Meta:
        verbose_name_plural = "Degrees"
        ordering = ['name']

    def __str__(self):
        return self.name

class College(TimeStampedModel):
    COLLEGE_TYPES = (
        ('eng', 'Engineering'),
        ('arts', 'Arts & Science'),
        ('med', 'Medical'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=255)
    university = models.CharField(max_length=255, blank=True, null=True, help_text="Name of affiliated university")
    college_type = models.CharField(max_length=10, choices=COLLEGE_TYPES, default=COLLEGE_TYPES[0][0])
    
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='colleges')
    degrees = models.ManyToManyField(Degree, related_name='colleges', blank=True)
    
    address_line = models.TextField(help_text="Street address, building name")
    pincode = models.CharField(max_length=10) 
    
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True) 

    latitude = models.DecimalField(
        max_digits=15, 
        decimal_places=10,
        null=True, 
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=15, 
        decimal_places=10, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    image = models.ImageField(upload_to='college_images', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="External image URL (used if image is not uploaded)")

    class Meta:
        verbose_name_plural = "Colleges"
        ordering = ['name']
        unique_together = ('name', 'district') 

    def __str__(self):
        return f"{self.name} ({self.district.name})"