from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import logging
from django.http import FileResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

logger = logging.getLogger(__name__)

def generate_pdf(cv):
    logger.info("Preparing context for PDF generation")
    # Lazy import to avoid circular dependency
    from .models import Education, Certificate, ProfessionalExperience, ProfessionalCompetency, Project, TechnicalSkill, Language, CommunityInvolvement, Award, Reference
    
    educations = cv.educations.all()
    experiences = cv.experiences.all()
    competencies = cv.competencies.all()
    projects = cv.projects.all()
    technical_skills = cv.technical_skills.first()
    languages = cv.languages.all()
    community_involvements = cv.community_involvements.all()
    awards = cv.awards.all()
    references = cv.references.all()

    pdf_path = os.path.join(settings.TEX_OUTPUT_DIR, f'cv_{cv.id}.pdf')
    os.makedirs(settings.TEX_OUTPUT_DIR, exist_ok=True)
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"CV for {cv.external_id}", styles['Heading1']))
    story.append(Paragraph(f"Submitted on: {cv.submitted_at.isoformat()}", styles['Normal']))
    story.append(Spacer(1, 12))

    if educations:
        story.append(Paragraph("Education", styles['Heading2']))
        for edu in educations:
            edu_text = f"{edu.degree_title} at {edu.university}, Expected: {edu.expected_graduation}"
            story.append(Paragraph(edu_text, styles['Normal']))
            for cert in edu.certificates.all():
                cert_text = f"- {cert.certificate_title} ({cert.year}, {cert.organization})"
                story.append(Paragraph(cert_text, styles['Normal']))
        story.append(Spacer(1, 12))

    if experiences:
        story.append(Paragraph("Professional Experience", styles['Heading2']))
        table_data = [["Position", "Company", "Dates", "Accomplishments"]]
        for exp in experiences:
            table_data.append([exp.position_title, exp.company, exp.dates, exp.accomplishments or "N/A"])
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

    if competencies:
        story.append(Paragraph("Competencies", styles['Heading2']))
        for comp in competencies:
            story.append(Paragraph(f"{comp.competency_type}: {comp.key_accomplishments}", styles['Normal']))
        story.append(Spacer(1, 12))

    if projects:
        story.append(Paragraph("Projects", styles['Heading2']))
        for proj in projects:
            story.append(Paragraph(f"{proj.project_title} ({proj.year}): {proj.summary}", styles['Normal']))
        story.append(Spacer(1, 12))

    if technical_skills:
        story.append(Paragraph("Technical Skills", styles['Heading2']))
        story.append(Paragraph(f"Languages: {technical_skills.programming_languages}", styles['Normal']))
        story.append(Paragraph(f"Frameworks: {technical_skills.frameworks_databases}", styles['Normal']))
        story.append(Paragraph(f"Tools: {technical_skills.tools}", styles['Normal']))
        story.append(Spacer(1, 12))

    if languages:
        story.append(Paragraph("Languages", styles['Heading2']))
        for lang in languages:
            story.append(Paragraph(f"- {lang.name}", styles['Normal']))
        story.append(Spacer(1, 12))

    if community_involvements:
        story.append(Paragraph("Community Involvement", styles['Heading2']))
        for ci in community_involvements:
            story.append(Paragraph(f"{ci.position_title} at {ci.organization}, {ci.dates}: {ci.achievements}", styles['Normal']))
        story.append(Spacer(1, 12))

    if awards:
        story.append(Paragraph("Awards", styles['Heading2']))
        for award in awards:
            story.append(Paragraph(f"{award.award_name} ({award.year}): {award.short_description or 'N/A'}", styles['Normal']))
        story.append(Spacer(1, 12))

    if references:
        story.append(Paragraph("References", styles['Heading2']))
        for ref in references:
            story.append(Paragraph(f"{ref.reference_name}, {ref.position}, {ref.email}, {ref.phone}", styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)
    return f'/media/pdfs/cv_{cv.id}.pdf'

class CVSubmitView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        logger.info("CVSubmitView.post called with data: %s", request.data)
        data = request.data
        email = data.get('email')
        external_id = data.get('external_id')
        if not all([email, external_id]):
            logger.error("Missing email or external_id")
            return Response({"error": "email and external_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Lazy import to avoid circular dependency
        from .models import CVSubmission
        
        if CVSubmission.objects.filter(external_id=external_id).exists():
            logger.warning("CV already exists for external_id: %s", external_id)
            return Response({"error": "CV already exists for this external ID"}, status=status.HTTP_400_BAD_REQUEST)

        cv = CVSubmission.objects.create(external_id=external_id)

        # Handle Education and Certificates
        from .models import Education, Certificate
        for edu_data in data.get('educations', []):
            education = Education.objects.create(cv=cv, **{k: v for k, v in edu_data.items() if k != 'certificates'})
            for cert_data in edu_data.get('certificates', []):
                Certificate.objects.create(education=education, **cert_data)

        # Handle other sections
        from .models import ProfessionalExperience, ProfessionalCompetency, Project, TechnicalSkill, Language, CommunityInvolvement, Award, Reference
        for exp_data in data.get('experiences', []):
            ProfessionalExperience.objects.create(cv=cv, **exp_data)
        for comp_data in data.get('competencies', []):
            ProfessionalCompetency.objects.create(cv=cv, **comp_data)
        for proj_data in data.get('projects', []):
            Project.objects.create(cv=cv, **proj_data)
        if 'technical_skills' in data:
            TechnicalSkill.objects.create(cv=cv, **data['technical_skills'])
        for lang_data in data.get('languages', []):
            Language.objects.create(cv=cv, **lang_data)
        for comm_data in data.get('community_involvements', []):
            CommunityInvolvement.objects.create(cv=cv, **comm_data)
        for award_data in data.get('awards', []):
            Award.objects.create(cv=cv, **award_data)
        for ref_data in data.get('references', []):
            Reference.objects.create(cv=cv, **ref_data)

        logger.info("Generating PDF for cv_id: %s", cv.id)
        pdf_path = generate_pdf(cv)
        logger.info("PDF generated at: %s", pdf_path)

        return Response({"message": "CV submitted", "cv_id": cv.id, "pdf_url": pdf_path}, status=status.HTTP_201_CREATED)
class CVPDFView(APIView):
    def get(self, request, cv_id):
        logger.info("CVPDFView.get called for cv_id: %s", cv_id)
        # Lazy import to avoid circular dependency
        from .models import CVSubmission
        try:
            cv = CVSubmission.objects.get(id=cv_id)
            pdf_path = os.path.join(settings.TEX_OUTPUT_DIR, f'cv_{cv.id}.pdf')
            if not os.path.exists(pdf_path):
                logger.error("PDF not found for cv_id: %s", cv_id)
                return Response({"error": "PDF not generated yet"}, status=status.HTTP_404_NOT_FOUND)
            return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename=f'cv_{cv.external_id}.pdf')
        except CVSubmission.DoesNotExist:
            logger.error("CV not found for cv_id: %s", cv_id)
            return Response({"error": "CV not found"}, status=status.HTTP_404_NOT_FOUND)

class CVEditView(APIView):
    parser_classes = [JSONParser]

    def get(self, request, cv_id):
        logger.info("CVEditView.get called for cv_id: %s", cv_id)
        # Lazy import to avoid circular dependency
        from .models import CVSubmission, Education, Certificate, ProfessionalExperience, ProfessionalCompetency, Project, TechnicalSkill, Language, CommunityInvolvement, Award, Reference
        try:
            cv = CVSubmission.objects.get(id=cv_id)
            data = {
                "external_id": cv.external_id,
                "educations": [
                    {
                        "id": edu.id,
                        "degree_title": edu.degree_title,
                        "university": edu.university,
                        "expected_graduation": edu.expected_graduation,
                        "certificates": [
                            {
                                "id": cert.id,
                                "certificate_title": cert.certificate_title,
                                "organization": cert.organization,
                                "year": cert.year
                            } for cert in edu.certificates.all()
                        ]
                    } for edu in cv.educations.all()
                ],
                "experiences": [
                    {
                        "id": exp.id,
                        "position_title": exp.position_title,
                        "company": exp.company,
                        "dates": exp.dates,
                        "accomplishments": exp.accomplishments
                    } for exp in cv.experiences.all()
                ],
                "competencies": [
                    {
                        "id": comp.id,
                        "competency_type": comp.competency_type,
                        "key_accomplishments": comp.key_accomplishments
                    } for comp in cv.competencies.all()
                ],
                "projects": [
                    {
                        "id": proj.id,
                        "project_title": proj.project_title,
                        "year": proj.year,
                        "summary": proj.summary
                    } for proj in cv.projects.all()
                ],
                "technical_skills": {
                    "id": technical_skills.id if technical_skills else None,
                    "programming_languages": technical_skills.programming_languages if technical_skills else "",
                    "frameworks_databases": technical_skills.frameworks_databases if technical_skills else "",
                    "tools": technical_skills.tools if technical_skills else ""
                } if (technical_skills := cv.technical_skills.first()) else {},
                "languages": [
                    {"id": lang.id, "name": lang.name} for lang in cv.languages.all()
                ],
                "community_involvements": [
                    {
                        "id": ci.id,
                        "position_title": ci.position_title,
                        "organization": ci.organization,
                        "dates": ci.dates,
                        "achievements": ci.achievements
                    } for ci in cv.community_involvements.all()
                ],
                "awards": [
                    {
                        "id": award.id,
                        "award_name": award.award_name,
                        "year": award.year,
                        "short_description": award.short_description
                    } for award in cv.awards.all()
                ],
                "references": [
                    {
                        "id": ref.id,
                        "reference_name": ref.reference_name,
                        "position": ref.position,
                        "email": ref.email,
                        "phone": ref.phone
                    } for ref in cv.references.all()
                ]
            }
            logger.info("CV details retrieved for editing cv_id: %s", cv_id)
            return Response(data, status=status.HTTP_200_OK)
        except CVSubmission.DoesNotExist:
            logger.error("CV not found for cv_id: %s", cv_id)
            return Response({"error": "CV not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, cv_id):
        logger.info("CVEditView.put called for cv_id: %s with data: %s", cv_id, request.data)
        # Lazy import to avoid circular dependency
        from .models import CVSubmission, Education, Certificate, ProfessionalExperience, ProfessionalCompetency, Project, TechnicalSkill, Language, CommunityInvolvement, Award, Reference
        try:
            cv = CVSubmission.objects.get(id=cv_id)
            data = request.data
            external_id = data.get('external_id', cv.external_id)
            if external_id != cv.external_id:
                cv.external_id = external_id
                cv.save()

            # Handle partial updates for educations
            for edu_data in data.get('educations', []):
                edu_id = edu_data.get('id')
                if edu_id:
                    education = Education.objects.get(id=edu_id, cv=cv)
                    for key, value in edu_data.items():
                        if key != 'id' and key != 'certificates':
                            setattr(education, key, value)
                    education.save()
                    # Update or create certificates
                    for cert_data in edu_data.get('certificates', []):
                        cert_id = cert_data.get('id')
                        if cert_id:
                            cert = Certificate.objects.get(id=cert_id, education=education)
                            for key, value in cert_data.items():
                                if key != 'id':
                                    setattr(cert, key, value)
                            cert.save()
                        else:
                            Certificate.objects.create(education=education, **{k: v for k, v in cert_data.items() if k != 'id'})
                else:
                    education = Education.objects.create(cv=cv, **{k: v for k, v in edu_data.items() if k != 'id' and k != 'certificates'})
                    for cert_data in edu_data.get('certificates', []):
                        Certificate.objects.create(education=education, **{k: v for k, v in cert_data.items() if k != 'id'})

            # Handle partial updates for other sections (similar pattern)
            for exp_data in data.get('experiences', []):
                exp_id = exp_data.get('id')
                if exp_id:
                    exp = ProfessionalExperience.objects.get(id=exp_id, cv=cv)
                    for key, value in exp_data.items():
                        if key != 'id':
                            setattr(exp, key, value)
                    exp.save()
                else:
                    ProfessionalExperience.objects.create(cv=cv, **{k: v for k, v in exp_data.items() if k != 'id'})

            for comp_data in data.get('competencies', []):
                comp_id = comp_data.get('id')
                if comp_id:
                    comp = ProfessionalCompetency.objects.get(id=comp_id, cv=cv)
                    for key, value in comp_data.items():
                        if key != 'id':
                            setattr(comp, key, value)
                    comp.save()
                else:
                    ProfessionalCompetency.objects.create(cv=cv, **{k: v for k, v in comp_data.items() if k != 'id'})

            for proj_data in data.get('projects', []):
                proj_id = proj_data.get('id')
                if proj_id:
                    proj = Project.objects.get(id=proj_id, cv=cv)
                    for key, value in proj_data.items():
                        if key != 'id':
                            setattr(proj, key, value)
                    proj.save()
                else:
                    Project.objects.create(cv=cv, **{k: v for k, v in proj_data.items() if k != 'id'})

            if 'technical_skills' in data:
                tech_data = data['technical_skills']
                tech_id = tech_data.get('id')
                if tech_id:
                    tech = TechnicalSkill.objects.get(id=tech_id, cv=cv)
                    for key, value in tech_data.items():
                        if key != 'id':
                            setattr(tech, key, value)
                    tech.save()
                else:
                    TechnicalSkill.objects.create(cv=cv, **{k: v for k, v in tech_data.items() if k != 'id'})

            for lang_data in data.get('languages', []):
                lang_id = lang_data.get('id')
                if lang_id:
                    lang = Language.objects.get(id=lang_id, cv=cv)
                    for key, value in lang_data.items():
                        if key != 'id':
                            setattr(lang, key, value)
                    lang.save()
                else:
                    Language.objects.create(cv=cv, **{k: v for k, v in lang_data.items() if k != 'id'})

            for comm_data in data.get('community_involvements', []):
                comm_id = comm_data.get('id')
                if comm_id:
                    comm = CommunityInvolvement.objects.get(id=comm_id, cv=cv)
                    for key, value in comm_data.items():
                        if key != 'id':
                            setattr(comm, key, value)
                    comm.save()
                else:
                    CommunityInvolvement.objects.create(cv=cv, **{k: v for k, v in comm_data.items() if k != 'id'})

            for award_data in data.get('awards', []):
                award_id = award_data.get('id')
                if award_id:
                    award = Award.objects.get(id=award_id, cv=cv)
                    for key, value in award_data.items():
                        if key != 'id':
                            setattr(award, key, value)
                    award.save()
                else:
                    Award.objects.create(cv=cv, **{k: v for k, v in award_data.items() if k != 'id'})

            for ref_data in data.get('references', []):
                ref_id = ref_data.get('id')
                if ref_id:
                    ref = Reference.objects.get(id=ref_id, cv=cv)
                    for key, value in ref_data.items():
                        if key != 'id':
                            setattr(ref, key, value)
                    ref.save()
                else:
                    Reference.objects.create(cv=cv, **{k: v for k, v in ref_data.items() if k != 'id'})

            logger.info("Regenerating PDF for cv_id: %s", cv.id)
            pdf_path = generate_pdf(cv)
            logger.info("PDF regenerated at: %s", pdf_path)

            return Response({"message": "CV updated", "cv_id": cv.id, "pdf_url": pdf_path}, status=status.HTTP_200_OK)
        except CVSubmission.DoesNotExist:
            logger.error("CV not found for cv_id: %s", cv_id)
            return Response({"error": "CV not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("Error updating CV %s: %s", cv_id, str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CVDetailView(APIView):
    def get(self, request, cv_id):
        logger.info("CVDetailView.get called for cv_id: %s", cv_id)
        # Lazy import to avoid circular dependency
        from .models import CVSubmission, Education, Certificate, ProfessionalExperience, ProfessionalCompetency, Project, TechnicalSkill, Language, CommunityInvolvement, Award, Reference
        try:
            cv = CVSubmission.objects.get(id=cv_id)
            data = {
                "external_id": cv.external_id,
                "submitted_at": cv.submitted_at.isoformat(),
                "educations": [
                    {
                        "degree_title": edu.degree_title,
                        "university": edu.university,
                        "expected_graduation": edu.expected_graduation,
                        "certificates": [
                            {
                                "certificate_title": cert.certificate_title,
                                "organization": cert.organization,
                                "year": cert.year
                            } for cert in edu.certificates.all()
                        ]
                    } for edu in cv.educations.all()
                ],
                "experiences": [
                    {
                        "position_title": exp.position_title,
                        "company": exp.company,
                        "dates": exp.dates,
                        "accomplishments": exp.accomplishments
                    } for exp in cv.experiences.all()
                ],
                "competencies": [
                    {
                        "competency_type": comp.competency_type,
                        "key_accomplishments": comp.key_accomplishments
                    } for comp in cv.competencies.all()
                ],
                "projects": [
                    {
                        "project_title": proj.project_title,
                        "year": proj.year,
                        "summary": proj.summary
                    } for proj in cv.projects.all()
                ],
                "technical_skills": {
                    "programming_languages": cv.technical_skills.first().programming_languages if cv.technical_skills.first() else "",
                    "frameworks_databases": cv.technical_skills.first().frameworks_databases if cv.technical_skills.first() else "",
                    "tools": cv.technical_skills.first().tools if cv.technical_skills.first() else ""
                } if cv.technical_skills.first() else {},
                "languages": [{"name": lang.name} for lang in cv.languages.all()],
                "community_involvements": [
                    {
                        "position_title": ci.position_title,
                        "organization": ci.organization,
                        "dates": ci.dates,
                        "achievements": ci.achievements
                    } for ci in cv.community_involvements.all()
                ],
                "awards": [
                    {
                        "award_name": award.award_name,
                        "year": award.year,
                        "short_description": award.short_description
                    } for award in cv.awards.all()
                ],
                "references": [
                    {
                        "reference_name": ref.reference_name,
                        "position": ref.position,
                        "email": ref.email,
                        "phone": ref.phone
                    } for ref in cv.references.all()
                ]
            }
            logger.info("CV details retrieved for cv_id: %s", cv_id)
            return Response(data, status=status.HTTP_200_OK)
        except CVSubmission.DoesNotExist:
            logger.error("CV not found for cv_id: %s", cv_id)
            return Response({"error": "CV not found"}, status=status.HTTP_404_NOT_FOUND)

class CVListView(APIView):
    def get(self, request):
        logger.info("CVListView.get called")
        from .models import CVSubmission
        cvs = CVSubmission.objects.all().prefetch_related('technical_skills', 'languages')
        serialized_data = [
            {
                'id': cv.id,
                'external_id': cv.external_id,
                'submitted_at': cv.submitted_at,
                'technical_skills': [
                    {
                        'programming_languages': ts.programming_languages,
                        'frameworks_databases': ts.frameworks_databases,
                        'tools': ts.tools
                    }
                    for ts in cv.technical_skills.all()
                ] if cv.technical_skills.exists() else [],
                'languages': [{'name': lang.name} for lang in cv.languages.all()] if cv.languages.exists() else []
            }
            for cv in cvs
        ]
        return Response(serialized_data, status=status.HTTP_200_OK)