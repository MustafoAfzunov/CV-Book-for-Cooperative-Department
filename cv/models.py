from django.db import models

class CVSubmission(models.Model):
    name = models.CharField(max_length=100)  # User's first name
    surname = models.CharField(max_length=100)  # User's last name
    email = models.EmailField(unique=True)  # Unique email as identifier
    major = models.CharField(max_length=100, blank=True, default='')  # User's major
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='processed')

    def __str__(self):
        return f"CV-{self.name} {self.surname}"

class Education(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='educations')
    degree_title = models.CharField(max_length=200, blank=True, default='')
    university = models.CharField(max_length=200, blank=True, default='')
    expected_graduation = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return f"{self.degree_title} at {self.university}" if self.university else self.degree_title

class Certificate(models.Model):
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='certificates')
    certificate_title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True, default='')
    year = models.CharField(max_length=4, blank=True, default='')

    def __str__(self):
        return self.certificate_title

class ProfessionalExperience(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='experiences')
    position_title = models.CharField(max_length=200, blank=True, default='')
    company = models.CharField(max_length=200, blank=True, default='')
    dates = models.CharField(max_length=50, blank=True, default='')
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
    year = models.CharField(max_length=4, blank=True, default='')
    summary = models.TextField(blank=True, default='')

    def __str__(self):
        return self.project_title

class TechnicalSkill(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='technical_skills')
    programming_languages = models.CharField(max_length=200, blank=True, default='')
    frameworks_databases = models.CharField(max_length=200, blank=True, default='')
    tools = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return f"Skills for {self.cv.name} {self.cv.surname}"

class Language(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CommunityInvolvement(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='community_involvements')
    position_title = models.CharField(max_length=200, blank=True, default='')
    organization = models.CharField(max_length=200, blank=True, default='')
    dates = models.CharField(max_length=50, blank=True, default='')
    achievements = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.position_title} at {self.organization}" if self.organization else self.position_title

class Award(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='awards')
    award_name = models.CharField(max_length=200)
    year = models.CharField(max_length=4, blank=True, default='')
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