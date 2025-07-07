// Global state
let currentStep = 1;
const totalSteps = 10;
let educationCount = 1;
let experienceCount = 1;
let competencyCount = 1;
let projectCount = 1;
let languageCount = 1;
let communityCount = 1;
let awardCount = 1;
let certificateCount = {};

function showStep(step) {
    document.querySelectorAll('.form-step').forEach(s => s.style.display = 'none');
    document.getElementById(`step-${step}`).style.display = 'block';
    document.getElementById('currentStep').textContent = step;
    document.getElementById('progressBar').children[step - 1].classList.add('active');
    document.getElementById('prevBtn').style.display = step > 1 ? 'inline-block' : 'none';
    document.getElementById('nextBtn').style.display = step < totalSteps ? 'inline-block' : 'none';
    document.getElementById('generateCvBtn').style.display = step === totalSteps ? 'inline-block' : 'none';

    if (step === 10) {
        populateReview();
    }
    console.log(`Showing step ${step}`);
}

function nextPrev(n) {
    if (validateStep(currentStep)) {
        currentStep += n;
        if (currentStep < 1) currentStep = 1;
        if (currentStep > totalSteps) currentStep = totalSteps;
        showStep(currentStep);
    }
}

function validateStep(step) {
    let isValid = true;
    const inputs = document.querySelectorAll(`#step-${step} input[required], #step-${step} textarea[required]`);
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.parentElement.parentElement.querySelector('.error-message').style.display = 'block';
            isValid = false;
        } else {
            input.parentElement.parentElement.querySelector('.error-message').style.display = 'none';
        }
    });
    console.log(`Validated step ${step}, isValid: ${isValid}`);
    return isValid;
}

function addEducation() {
    educationCount++;
    const container = document.getElementById('educationContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'education-entry';
    newEntry.id = `education-${educationCount}`;
    newEntry.innerHTML = `
        <div class="row">
            <div class="form-group">
                <label for="degreeTitle${educationCount}">Degree Title *</label>
                <div class="input-group">
                    <i class="fas fa-graduation-cap"></i>
                    <input type="text" id="degreeTitle${educationCount}" name="degreeTitle${educationCount}" required placeholder="Enter your degree title">
                </div>
                <div class="error-message">This field is required</div>
            </div>
            <div class="form-group">
                <label for="university${educationCount}">University *</label>
                <div class="input-group">
                    <i class="fas fa-university"></i>
                    <input type="text" id="university${educationCount}" name="university${educationCount}" required placeholder="Enter your university">
                </div>
                <div class="error-message">This field is required</div>
            </div>
        </div>
        <div class="row">
            <div class="form-group">
                <label for="expectedGraduation${educationCount}">Expected Graduation *</label>
                <div class="input-group">
                    <i class="fas fa-calendar"></i>
                    <input type="text" id="expectedGraduation${educationCount}" name="expectedGraduation${educationCount}" required placeholder="e.g., 2025 or June 2025">
                </div>
                <div class="error-message">This field is required</div>
            </div>
        </div>
        <div id="certificateContainer${educationCount}"></div>
        <button type="button" class="add-btn" onclick="addCertificate(${educationCount})">+ Add Certificate</button>
        <button type="button" class="remove-btn" onclick="removeEducation(this)">- Remove</button>
    `;
    container.appendChild(newEntry);
    console.log(`Added education entry ${educationCount}`);
}

function removeEducation(button) {
    const entry = button.parentElement;
    entry.remove();
    educationCount--;
    console.log(`Removed education entry`);
}

function addCertificate(eduIndex) {
    if (!certificateCount[eduIndex]) certificateCount[eduIndex] = 0;
    certificateCount[eduIndex]++;
    const container = document.getElementById(`certificateContainer${eduIndex}`);
    const newCert = document.createElement('div');
    newCert.className = 'certificate-entry';
    newCert.id = `certificate-${eduIndex}-${certificateCount[eduIndex]}`;
    newCert.innerHTML = `
        <div class="row">
            <div class="form-group">
                <label for="certificateTitle${eduIndex}-${certificateCount[eduIndex]}">Certificate Title *</label>
                <div class="input-group">
                    <i class="fas fa-certificate"></i>
                    <input type="text" id="certificateTitle${eduIndex}-${certificateCount[eduIndex]}" name="certificateTitle${eduIndex}-${certificateCount[eduIndex]}" required placeholder="Enter certificate title">
                </div>
                <div class="error-message">This field is required</div>
            </div>
            <div class="form-group">
                <label for="organization${eduIndex}-${certificateCount[eduIndex]}">Organization</label>
                <div class="input-group">
                    <i class="fas fa-building"></i>
                    <input type="text" id="organization${eduIndex}-${certificateCount[eduIndex]}" name="organization${eduIndex}-${certificateCount[eduIndex]}" placeholder="Enter organization">
                </div>
            </div>
        </div>
        <div class="row">
            <div class="form-group">
                <label for="year${eduIndex}-${certificateCount[eduIndex]}">Year</label>
                <div class="input-group">
                    <i class="fas fa-calendar"></i>
                    <input type="text" id="year${eduIndex}-${certificateCount[eduIndex]}" name="year${eduIndex}-${certificateCount[eduIndex]}" placeholder="e.g., 2023">
                </div>
            </div>
            <button type="button" class="remove-btn" onclick="removeCertificate(this, ${eduIndex})">- Remove</button>
        </div>
    `;
    container.appendChild(newCert);
    console.log(`Added certificate for education ${eduIndex}`);
}

function removeCertificate(button, eduIndex) {
    const entry = button.parentElement.parentElement;
    entry.remove();
    certificateCount[eduIndex]--;
    console.log(`Removed certificate for education ${eduIndex}`);
}

function addExperience() {
    experienceCount++;
    const container = document.getElementById('experienceContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'experience-entry';
    newEntry.id = `experience-${experienceCount}`;
    newEntry.innerHTML = `
        <div class="row">
            <div class="form-group">
                <label for="positionTitle${experienceCount}">Position Title *</label>
                <div class="input-group">
                    <i class="fas fa-briefcase"></i>
                    <input type="text" id="positionTitle${experienceCount}" name="positionTitle${experienceCount}" required placeholder="Enter your position">
                </div>
                <div class="error-message">This field is required</div>
            </div>
            <div class="form-group">
                <label for="company${experienceCount}">Company *</label>
                <div class="input-group">
                    <i class="fas fa-building"></i>
                    <input type="text" id="company${experienceCount}" name="company${experienceCount}" required placeholder="Enter your company">
                </div>
                <div class="error-message">This field is required</div>
            </div>
        </div>
        <div class="row">
            <div class="form-group">
                <label for="dates${experienceCount}">Dates *</label>
                <div class="input-group">
                    <i class="fas fa-calendar"></i>
                    <input type="text" id="dates${experienceCount}" name="dates${experienceCount}" required placeholder="e.g., 2023-2024">
                </div>
                <div class="error-message">This field is required</div>
            </div>
            <div class="form-group">
                <label for="accomplishments${experienceCount}">Accomplishments</label>
                <div class="input-group">
                    <i class="fas fa-list"></i>
                    <textarea id="accomplishments${experienceCount}" name="accomplishments${experienceCount}" placeholder="List your accomplishments"></textarea>
                </div>
            </div>
        </div>
        <button type="button" class="remove-btn" onclick="removeExperience(this)">- Remove</button>
    `;
    container.appendChild(newEntry);
    console.log(`Added experience entry ${experienceCount}`);
}

function removeExperience(button) {
    const entry = button.parentElement;
    entry.remove();
    experienceCount--;
    console.log(`Removed experience entry`);
}

function addCompetency() {
    competencyCount++;
    const container = document.getElementById('competencyContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'competency-entry';
    newEntry.id = `competency-${competencyCount}`;
    newEntry.innerHTML = `
        <div class="row">
            <div class="form-group">
                <label for="competencyType${competencyCount}">Competency Type *</label>
                <div class="input-group">
                    <i class="fas fa-star"></i>
                    <input type="text" id="competencyType${competencyCount}" name="competencyType${competencyCount}" required placeholder="e.g., Leadership">
                </div>
                <div class="error-message">This field is required</div>
            </div>
            <div class="form-group">
                <label for="keyAccomplishments${competencyCount}">Key Accomplishments</label>
                <div class="input-group">
                    <i class="fas fa-list"></i>
                    <textarea id="keyAccomplishments${competencyCount}" name="keyAccomplishments${competencyCount}" placeholder="Describe your accomplishments"></textarea>
                </div>
            </div>
        </div>
        <button type="button" class="remove-btn" onclick="removeCompetency(this)">- Remove</button>
    `;
    container.appendChild(newEntry);
    console.log(`Added competency entry ${competencyCount}`);
}

function removeCompetency(button) {
    const entry = button.parentElement;
    entry.remove();
    competencyCount--;
    console.log(`Removed competency entry`);
}

function addProject() {
    projectCount++;
    const container = document.getElementById('projectContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'project-entry';
    newEntry.id = `project-${projectCount}`;
    newEntry.innerHTML = `
        <div class="row">
            <div class="form-group">
                <label for="projectTitle${projectCount}">Project Title *</label>
                <div class="input-group">
                    <i class="fas fa-project-diagram"></i>
                    <input type="text" id="projectTitle${projectCount}" name="projectTitle${projectCount}" required placeholder="Enter project title">
                </div>
                <div class="error-message">This field is required</div>
            </div>
            <div class="form-group">
                <label for="year${projectCount}">Year *</label>
                <div class="input-group">
                    <i class="fas fa-calendar"></i>
                    <input type="text" id="year${projectCount}" name="year${projectCount}" required placeholder="e.g., 2023">
                </div>
                <div class="error-message">This field is required</div>
            </div>
        </div>
        <div class="row">
            <div class="form-group">
                <label for="summary${projectCount}">Summary</label>
                <div class="input-group">
                    <i class="fas fa-list"></i>
                    <textarea id="summary${projectCount}" name="summary${projectCount}" placeholder="Brief project summary"></textarea>
                </div>
            </div>
        </div>
        <button type="button" class="remove-btn" onclick="removeProject(this)">- Remove</button>
    `;
    container.appendChild(newEntry);
    console.log(`Added project entry ${projectCount}`);
}

function removeProject(button) {
    const entry = button.parentElement;
    entry.remove();
    projectCount--;
    console.log(`Removed project entry`);
}

function addLanguage() {
    languageCount++;
    const container = document.getElementById('languageContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'language-entry';
    newEntry.id = `language-${languageCount}`;
    newEntry.innerHTML = `
        <div class="row">
            <div class="form-group">
                <label for="languageName${languageCount}">Language Name *</label>
                <div class="input-group">
                    <i class="fas fa-language"></i>
                    <input type="text" id="languageName${languageCount}" name="languageName${languageCount}" required placeholder="e.g., English">
                </div>
                <div class="error-message">This field is required</div>
            </div>
        </div>
        <button type="button" class="remove-btn" onclick="removeLanguage(this)">- Remove</button>
    `;
    container.appendChild(newEntry);
    console.log(`Added language entry ${languageCount}`);
}

function removeLanguage(button) {
    const entry = button.parentElement;
    entry.remove();
    languageCount--;
    console.log(`Removed language entry`);
}

function addCommunity() {
    communityCount++;
    const container = document.getElementById('communityContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'community-entry';
    newEntry.id = `community-${communityCount}`;
    newEntry.innerHTML = `
        <div class="row">
            <div class="form-group">
                <label for="positionTitle${communityCount}">Position Title</label>
                <div class="input-group">
                    <i class="fas fa-users"></i>
                    <input type="text" id="positionTitle${communityCount}" name="positionTitle${communityCount}" placeholder="e.g., Volunteer">
                </div>
            </div>
            <div class="form-group">
                <label for="organization${communityCount}">Organization</label>
                <div class="input-group">
                    <i class="fas fa-building"></i>
                    <input type="text" id="organization${communityCount}" name="organization${communityCount}" placeholder="e.g., Red Cross">
                </div>
            </div>
        </div>
        <div class="row">
            <div class="form-group">
                <label for="dates${communityCount}">Dates</label>
                <div class="input-group">
                    <i class="fas fa-calendar"></i>
                    <input type="text" id="dates${communityCount}" name="dates${communityCount}" placeholder="e.g., 2023-2024">
                </div>
            </div>
            <div class="form-group">
                <label for="achievements${communityCount}">Achievements</label>
                <div class="input-group">
                    <i class="fas fa-list"></i>
                    <textarea id="achievements${communityCount}" name="achievements${communityCount}" placeholder="Describe achievements"></textarea>
                </div>
            </div>
        </div>
        <button type="button" class="remove-btn" onclick="removeCommunity(this)">- Remove</button>
    `;
    container.appendChild(newEntry);
    console.log(`Added community entry ${communityCount}`);
}

function removeCommunity(button) {
    const entry = button.parentElement;
    entry.remove();
    communityCount--;
    console.log(`Removed community entry`);
}

function addAward() {
    awardCount++;
    const container = document.getElementById('awardContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'award-entry';
    newEntry.id = `award-${awardCount}`;
    newEntry.innerHTML = `
        <div class="row">
            <div class="form-group">
                <label for="awardName${awardCount}">Award Name *</label>
                <div class="input-group">
                    <i class="fas fa-trophy"></i>
                    <input type="text" id="awardName${awardCount}" name="awardName${awardCount}" required placeholder="Enter award name">
                </div>
                <div class="error-message">This field is required</div>
            </div>
            <div class="form-group">
                <label for="year${awardCount}">Year *</label>
                <div class="input-group">
                    <i class="fas fa-calendar"></i>
                    <input type="text" id="year${awardCount}" name="year${awardCount}" required placeholder="e.g., 2023">
                </div>
                <div class="error-message">This field is required</div>
            </div>
        </div>
        <div class="row">
            <div class="form-group">
                <label for="shortDescription${awardCount}">Short Description</label>
                <div class="input-group">
                    <i class="fas fa-list"></i>
                    <textarea id="shortDescription${awardCount}" name="shortDescription${awardCount}" placeholder="Brief description"></textarea>
                </div>
            </div>
        </div>
        <button type="button" class="remove-btn" onclick="removeAward(this)">- Remove</button>
    `;
    container.appendChild(newEntry);
    console.log(`Added award entry ${awardCount}`);
}

function removeAward(button) {
    const entry = button.parentElement;
    entry.remove();
    awardCount--;
    console.log(`Removed award entry`);
}

function saveDraft() {
    showMessage('Draft saved (feature not implemented yet)', 'success');
    console.log('Draft saved');
}

function clearForm() {
    if (confirm('Are you sure you want to clear the form?')) {
        document.getElementById('cvForm').reset();
        educationCount = 1;
        experienceCount = 1;
        competencyCount = 1;
        projectCount = 1;
        languageCount = 1;
        communityCount = 1;
        awardCount = 1;
        certificateCount = {};
        document.getElementById('educationContainer').innerHTML = document.getElementById('education-1').outerHTML;
        document.getElementById('experienceContainer').innerHTML = document.getElementById('experience-1').outerHTML;
        document.getElementById('competencyContainer').innerHTML = document.getElementById('competency-1').outerHTML;
        document.getElementById('projectContainer').innerHTML = document.getElementById('project-1').outerHTML;
        document.getElementById('languageContainer').innerHTML = document.getElementById('language-1').outerHTML;
        document.getElementById('communityContainer').innerHTML = document.getElementById('community-1').outerHTML;
        document.getElementById('awardContainer').innerHTML = document.getElementById('award-1').outerHTML;
        showStep(1);
        console.log('Form cleared');
    }
}

function populateReview() {
    const reviewInfo = document.getElementById('reviewInfo');
    reviewInfo.innerHTML = `
        <h4>Personal Information</h4>
        <p>Name: ${document.getElementById('name').value}</p>
        <p>Surname: ${document.getElementById('surname').value}</p>
        <p>Email: ${document.getElementById('email').value}</p>
        <h4>Education</h4>
        ${Array.from({ length: educationCount }, (_, i) => `
            <p><strong>${document.getElementById(`degreeTitle${i + 1}`).value || 'N/A'}</strong> at ${document.getElementById(`university${i + 1}`).value || 'N/A'}, Expected: ${document.getElementById(`expectedGraduation${i + 1}`).value || 'N/A'}</p>
            ${certificateCount[i + 1] ? Array.from({ length: certificateCount[i + 1] }, (_, j) => `
                <p>- ${document.getElementById(`certificateTitle${i + 1}-${j + 1}`).value || 'N/A'} (${document.getElementById(`year${i + 1}-${j + 1}`).value || 'N/A'})</p>
            `).join('') : ''}
        `).join('')}
        <h4>Professional Experience</h4>
        ${Array.from({ length: experienceCount }, (_, i) => `
            <p><strong>${document.getElementById(`positionTitle${i + 1}`).value || 'N/A'}</strong> at ${document.getElementById(`company${i + 1}`).value || 'N/A'}, ${document.getElementById(`dates${i + 1}`).value || 'N/A'}</p>
            <p>Accomplishments: ${document.getElementById(`accomplishments${i + 1}`).value || 'N/A'}</p>
        `).join('')}
        <h4>Professional Competencies</h4>
        ${Array.from({ length: competencyCount }, (_, i) => `
            <p><strong>${document.getElementById(`competencyType${i + 1}`).value || 'N/A'}</strong>: ${document.getElementById(`keyAccomplishments${i + 1}`).value || 'N/A'}</p>
        `).join('')}
        <h4>Projects</h4>
        ${Array.from({ length: projectCount }, (_, i) => `
            <p><strong>${document.getElementById(`projectTitle${i + 1}`).value || 'N/A'}</strong> (${document.getElementById(`year${i + 1}`).value || 'N/A'}): ${document.getElementById(`summary${i + 1}`).value || 'N/A'}</p>
        `).join('')}
        <h4>Technical Skills</h4>
        <p>Programming Languages: ${document.getElementById('programmingLanguages').value || 'N/A'}</p>
        <p>Frameworks/Databases: ${document.getElementById('frameworksDatabases').value || 'N/A'}</p>
        <p>Tools: ${document.getElementById('tools').value || 'N/A'}</p>
        <h4>Spoken Languages</h4>
        ${Array.from({ length: languageCount }, (_, i) => `
            <p>${document.getElementById(`languageName${i + 1}`).value || 'N/A'}</p>
        `).join('')}
        <h4>Community Involvement</h4>
        ${Array.from({ length: communityCount }, (_, i) => `
            <p><strong>${document.getElementById(`positionTitle${i + 1}`).value || 'N/A'}</strong> at ${document.getElementById(`organization${i + 1}`).value || 'N/A'}, ${document.getElementById(`dates${i + 1}`).value || 'N/A'}</p>
            <p>Achievements: ${document.getElementById(`achievements${i + 1}`).value || 'N/A'}</p>
        `).join('')}
        <h4>Awards</h4>
        ${Array.from({ length: awardCount }, (_, i) => `
            <p><strong>${document.getElementById(`awardName${i + 1}`).value || 'N/A'}</strong> (${document.getElementById(`year${i + 1}`).value || 'N/A'}): ${document.getElementById(`shortDescription${i + 1}`).value || 'N/A'}</p>
        `).join('')}
    `;
    console.log('Review populated');
}

document.getElementById('cvForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = {
        name: document.getElementById('name').value,
        surname: document.getElementById('surname').value,
        email: document.getElementById('email').value,
        educations: Array.from({ length: educationCount }, (_, i) => ({
            degree_title: document.getElementById(`degreeTitle${i + 1}`).value,
            university: document.getElementById(`university${i + 1}`).value,
            expected_graduation: document.getElementById(`expectedGraduation${i + 1}`).value,
            certificates: certificateCount[i + 1] ? Array.from({ length: certificateCount[i + 1] }, (_, j) => ({
                certificate_title: document.getElementById(`certificateTitle${i + 1}-${j + 1}`).value,
                organization: document.getElementById(`organization${i + 1}-${j + 1}`).value,
                year: document.getElementById(`year${i + 1}-${j + 1}`).value
            })) : []
        })),
        experiences: Array.from({ length: experienceCount }, (_, i) => ({
            position_title: document.getElementById(`positionTitle${i + 1}`).value,
            company: document.getElementById(`company${i + 1}`).value,
            dates: document.getElementById(`dates${i + 1}`).value,
            accomplishments: document.getElementById(`accomplishments${i + 1}`).value
        })),
        competencies: Array.from({ length: competencyCount }, (_, i) => ({
            competency_type: document.getElementById(`competencyType${i + 1}`).value,
            key_accomplishments: document.getElementById(`keyAccomplishments${i + 1}`).value
        })),
        projects: Array.from({ length: projectCount }, (_, i) => ({
            project_title: document.getElementById(`projectTitle${i + 1}`).value,
            year: document.getElementById(`year${i + 1}`).value,
            summary: document.getElementById(`summary${i + 1}`).value
        })),
        technical_skills: {
            programming_languages: document.getElementById('programmingLanguages').value,
            frameworks_databases: document.getElementById('frameworksDatabases').value,
            tools: document.getElementById('tools').value
        },
        languages: Array.from({ length: languageCount }, (_, i) => ({
            name: document.getElementById(`languageName${i + 1}`).value
        })),
        community_involvements: Array.from({ length: communityCount }, (_, i) => ({
            position_title: document.getElementById(`positionTitle${i + 1}`).value,
            organization: document.getElementById(`organization${i + 1}`).value,
            dates: document.getElementById(`dates${i + 1}`).value,
            achievements: document.getElementById(`achievements${i + 1}`).value
        })),
        awards: Array.from({ length: awardCount }, (_, i) => ({
            award_name: document.getElementById(`awardName${i + 1}`).value,
            year: document.getElementById(`year${i + 1}`).value,
            short_description: document.getElementById(`shortDescription${i + 1}`).value
        })),
        references: [] // Add reference logic if needed
    };

    fetch('http://127.0.0.1:8000/cv/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to submit CV');
        return response.json();
    })
    .then(data => {
        showMessage('CV submitted successfully!', 'success');
        console.log('CV submitted:', data);
        window.location.href = `/cv/${data.cv_id}/`;
    })
    .catch(error => showMessage(`Error submitting CV: ${error.message}`, 'error'));
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showMessage(text, type) {
    const message = document.getElementById('message') || document.createElement('div');
    if (!document.getElementById('message')) {
        message.id = 'message';
        message.style.cssText = 'position: fixed; top: 10px; left: 50%; transform: translateX(-50%); padding: 10px; background: #333; color: #fff; border-radius: 5px; z-index: 1000; display: none;';
        document.body.appendChild(message);
    }
    message.textContent = text;
    message.className = type; // Assume CSS classes like 'success', 'error', 'info' are defined
    message.style.display = 'block';
    setTimeout(() => message.style.display = 'none', 5000);
    console.log(`Message shown: ${text}, type: ${type}`);
}

document.addEventListener('DOMContentLoaded', () => {
    showStep(currentStep);
    document.getElementById('cvFormModal').style.display = 'block';
});