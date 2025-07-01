from django.db import models

class CVRequest(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # No default, no null
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.status}"

class CVSubmission(models.Model):
    external_id = models.CharField(max_length=100, unique=True)  # ID from the larger platform
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, processed
    request = models.ForeignKey(CVRequest, on_delete=models.CASCADE, null=True, blank=True)  # Link to CVRequest instead of User

    def __str__(self):
        return f"CV-{self.external_id}"

class Education(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='educations')
    degree_title = models.CharField(max_length=200, blank=True, default='')
    university = models.CharField(max_length=200, blank=True, default='')  # Allow blank
    expected_graduation = models.CharField(max_length=50, blank=True, default='')  # Could be date or year
    
    def __str__(self):
        return f"{self.degree_title} at {self.university}" if self.university else self.degree_title

class Certificate(models.Model):
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='certificates')
    certificate_title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True, default='')
    year = models.CharField(max_length=4, blank=True, default='')  # Assuming year as string (e.g., "2023")
    
    def __str__(self):
        return self.certificate_title

class ProfessionalExperience(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='experiences')
    position_title = models.CharField(max_length=200, blank=True, default='')
    company = models.CharField(max_length=200, blank=True, default='')
    dates = models.CharField(max_length=50, blank=True, default='')  # e.g., "2020-2022"
    accomplishments = models.TextField(blank=True, default='')
    
    def __str__(self):
        return f"{self.position_title} at {self.company}" if self.company else self.position_title

class ProfessionalCompetency(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='competencies')
    competency_type = models.CharField(max_length=200)
    key_accomplishments = models.TextField(blank=True, default='')
    
    def __str__(self):
        return self.competency_type

class Project(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='projects')
    project_title = models.CharField(max_length=200)
    year = models.CharField(max_length=4, blank=True, default='')  # Assuming year as string
    summary = models.TextField(blank=True, default='')
    
    def __str__(self):
        return self.project_title

class TechnicalSkill(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='technical_skills')
    programming_languages = models.CharField(max_length=200, blank=True, default='')
    frameworks_databases = models.CharField(max_length=200, blank=True, default='')
    tools = models.CharField(max_length=200, blank=True, default='')
    
    def __str__(self):
        return f"Skills for {self.cv.external_id}"

class Language(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class CommunityInvolvement(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='community_involvements')
    position_title = models.CharField(max_length=200, blank=True, default='')
    organization = models.CharField(max_length=200, blank=True, default='')
    dates = models.CharField(max_length=50, blank=True, default='')  # e.g., "2020-2022"
    achievements = models.TextField(blank=True, default='')
    
    def __str__(self):
        return f"{self.position_title} at {self.organization}" if self.organization else self.position_title

class Award(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='awards')
    award_name = models.CharField(max_length=200)
    year = models.CharField(max_length=4, blank=True, default='')  # Assuming year as string
    short_description = models.TextField(blank=True, default='')
    
    def __str__(self):
        return self.award_name

class Reference(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='references')
    reference_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=15, blank=True, default='')
    
    def __str__(self):
        return self.reference_name