// Global state
let cvsData = [];

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

function loadCVs() {
    fetch('http://127.0.0.1:8000/cv/list/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        console.log('CV list response status:', response.status);
        if (!response.ok) throw new Error('Failed to load CVs: ' + response.statusText);
        return response.json();
    })
    .then(data => {
        cvsData = data;
        renderCards(cvsData);
    })
    .catch(error => showMessage(`Error loading CVs: ${error.message}`, 'error'));
}

function renderCards(data) {
    const grid = document.getElementById('student-grid');
    grid.innerHTML = '';
    if (data.length === 0) {
        grid.innerHTML = '<p>No CVs available at the moment. Generate a CV to get started.</p>';
        return;
    }
    data.forEach(cv => {
        const card = document.createElement('div');
        card.className = 'student-card';
        card.dataset.category = getCategoryFromSkills(cv) || 'all';
        card.innerHTML = `
            <div class="student-name">${cv.external_id || 'Unknown ID'}</div>
            <div class="student-major">${getMajorFromSkills(cv) || 'CV Details'}</div>
            <div class="card-actions">
                <a href="/cv/${cv.id}/download/" class="action-btn">Download</a>
                <a href="/cv/${cv.id}/edit/" class="action-btn">Edit</a>
            </div>
        `;
        card.onclick = () => window.location.href = `/cv/${cv.id}/`;
        grid.appendChild(card);
    });
}

function getCategoryFromSkills(cv) {
    if (cv.technical_skills?.programming_languages) return 'computer-science';
    if (cv.technical_skills?.frameworks_databases) return 'communication-media';
    return 'global-economics'; // Default category
}

function getMajorFromSkills(cv) {
    if (cv.technical_skills?.programming_languages) return 'Computer Science';
    if (cv.technical_skills?.frameworks_databases) return 'Communication and Media';
    return 'Global Economics'; // Default major
}

function filterCards() {
    const activeTab = document.querySelector('.filter-tab.active').dataset.filter;
    const country = document.querySelector('.dropdown:nth-child(1)').value;
    const language = document.querySelector('.dropdown:nth-child(2)').value;
    const techSkill = document.querySelector('.dropdown:nth-child(3)').value;
    const nonTechSkill = document.querySelector('.dropdown:nth-child(4)').value;
    const sortOrder = document.querySelector('.dropdown:nth-child(5)').value;
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    let filteredData = cvsData.filter(cv => {
        const matchesCategory = activeTab === 'all' || cv.dataset.category === activeTab;
        const matchesCountry = !country || cv.country === country; // Adjust based on backend data
        const matchesLanguage = !language || cv.languages?.some(l => l.name === language);
        const matchesTechSkill = !techSkill || cv.technical_skills?.[techSkill.toLowerCase().replace(' ', '_')] === techSkill;
        const matchesNonTechSkill = !nonTechSkill || cv.competencies?.some(c => c.competency_type === nonTechSkill);
        const matchesSearch = !searchTerm || cv.external_id.toLowerCase().includes(searchTerm);

        return matchesCategory && matchesCountry && matchesLanguage && matchesTechSkill && matchesNonTechSkill && matchesSearch;
    });

    if (sortOrder === 'desc') {
        filteredData.sort((a, b) => (b.external_id || '').localeCompare(a.external_id || ''));
    } else {
        filteredData.sort((a, b) => (a.external_id || '').localeCompare(b.external_id || ''));
    }

    renderCards(filteredData);
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded and initialized');

    // Load CVs on page load
    if (window.location.pathname.includes('/cv/cards/')) {
        loadCVs();
    }

    // Filter tab click handlers
    document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            filterCards();
        });
    });

    // Dropdown and search input change handlers
    document.querySelectorAll('.dropdown, #searchInput').forEach(element => {
        element.addEventListener('change', filterCards);
    });
});

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