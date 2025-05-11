
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import RegexValidator, URLValidator, EmailValidator
from ckeditor.fields import RichTextField


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    
    description = RichTextField(blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{4,10}$')],
        help_text="Enter a valid pincode (4 to 10 digits)"
    )

    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{7,15}$')],
        help_text="Enter phone in format: '+919999999999'"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        validators=[EmailValidator()]
    )
    website = models.URLField(blank=True, null=True, validators=[URLValidator()])

    # Geo location fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, help_text="Latitude coordinate of the location (e.g., 12.971599).")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,help_text="Longitude coordinate of the location (e.g., 77.594566).")

    opened_on = models.DateField(help_text="The date when the hospital was opened")
    license_number = models.CharField(max_length=255, blank=True, null=True, help_text="License number of the hospital")
    license_issued_on = models.DateField(blank=True, null=True, help_text="Date when the hospital license was issued")
    license_expires_on = models.DateField(blank=True, null=True, help_text="Date when the hospital license expires")
    license_status = models.CharField(
        max_length=50,
        choices=[('ACTIVE', 'Active'), ('EXPIRED', 'Expired'), ('REVOKED', 'Revoked')],
        default='ACTIVE',
        help_text="The current status of the hospital's license"
    )
    closed_on=models.DateField(null=True,blank=True,help_text="The date when the hospital was opened")
    hp_closed=models.BooleanField(null=True,blank=True)
    
    # Audit and status
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hospitals_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hospitals_updated'
    )

    class Meta:
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['state']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Hospital, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class HospitalImage(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='hospital_images/')
    caption = models.CharField(max_length=255, blank=True)
    sequence = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hospitals_img_uploadeded_by'
    )

    class Meta:
        ordering = ['sequence', 'uploaded_at']  # ensures sorted images

    def __str__(self):
        return f"Image {self.sequence} of {self.hospital.name}"
    


class HospitalReview(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together = ('hospital', 'user')  # Prevent multiple reviews per user per hospital
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.hospital.name} - {self.user} ({self.rating}⭐)"
    

APPOINTMENT_STATUS_CHOICES = [
    (1, "Pending"),
    (2, "Confirmed"),
    (3, "Cancelled"),
    (4, "Completed"),
    (5, "No Show"),
]


class Appointment(models.Model):

    hospital = models.ForeignKey("Hospital", on_delete=models.CASCADE, related_name="appointments_hospital")
    doctor = models.ForeignKey("core.CustomUser", on_delete=models.CASCADE, related_name="doctor_appointments")
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments_patient")

    appointment_date = models.DateField()
    appointment_start_time = models.TimeField()
    appointment_end_time = models.TimeField()

    symptoms = models.TextField(blank=True, null=True, help_text="Short description of patient symptoms or concerns.")
    notes = models.TextField(blank=True, null=True, help_text="Doctor or admin notes for internal use.")

    status = models.PositiveIntegerField(
        choices=APPOINTMENT_STATUS_CHOICES,
        default=1
    )


    booking_reference = models.CharField(
        max_length=20, unique=True, help_text="Unique booking reference number"
    )

    is_paid = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments_updated'
    )

    class Meta:
        unique_together = ('doctor', 'appointment_date', 'appointment_start_time')
        ordering = ['-appointment_date', '-appointment_start_time']

    def __str__(self):
        return f"Appointment #{self.booking_reference} - {self.patient} with {self.doctor} at {self.hospital}"

    def is_past_due(self):
        return timezone.now().date() > self.appointment_date
    
class DoctorHospitalAssociation(models.Model):
    doctor = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE,related_name="doctor_association_with")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE,related_name="hospital_association_with")
    
    # Additional fields to store the relationship between doctor and hospital
    date_joined = models.DateField(help_text="Date the doctor joined the hospital")

    role = models.CharField(max_length=100, choices=[
        ('Consultant', 'Consultant'),
        ('Specialist', 'Specialist'),
        ('Resident', 'Resident'),
        ('Visiting', 'Visiting'),
    ], help_text="Doctor's role in the hospital")
    
    is_active = models.BooleanField(default=True, help_text="Whether the doctor is currently active in the hospital")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('doctor', 'hospital')  # Ensures a doctor can't belong to the same hospital twice

    def __str__(self):
        return f"{self.doctor} - {self.hospital} ({self.role})"