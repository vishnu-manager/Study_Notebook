const subjectsByBranch = {
  "CSE": {
    "1st Year": ["Mathematics", "Programming", "Physics"],
    "2nd Year": ["Data Structures", "DBMS", "OOP"],
    "3rd Year": ["AI", "ML", "Networks"],
    "4th Year": ["Cloud", "Blockchain", "IoT"]
  },
  "CIVIL": {
    "1st Year": ["Engineering Mechanics", "Math"],
    "2nd Year": ["Structural Analysis", "Concrete Tech"],
    "3rd Year": ["Water Resources", "Geotechnical Engg"],
    "4th Year": ["Construction Mgmt", "Estimating"]
  },
  "MECH": {
    "1st Year": ["Math", "Engineering Drawing"],
    "2nd Year": ["Thermodynamics", "Fluid Mechanics"],
    "3rd Year": ["Machine Design", "Heat Transfer"],
    "4th Year": ["CAD/CAM", "Robotics"]
  },
  "EEE": {
    "1st Year": ["Basic Electrical", "Math"],
    "2nd Year": ["Electromagnetics", "Circuit Theory"],
    "3rd Year": ["Power Systems", "Machines"],
    "4th Year": ["Renewable Energy", "Control Systems"]
  }
};

function showSubjects(course) {
  fetch(`/get_pdfs/${course}`)
    .then(response => response.json())
    .then(data => {
      const subjectArea = document.getElementById('subjectArea');
      subjectArea.innerHTML = `<h2>${course} Subjects</h2>`;
      if (data.length === 0) {
        subjectArea.innerHTML += "<p>No PDFs uploaded for this course.</p>";
        return;
      }
      data.forEach(item => {
        const link = document.createElement('a');
        link.textContent = `${item.subject} (${item.year})`;
        link.href = '#';
        link.onclick = () => openModal(item.pdf_url);
        link.style.display = 'block';
        subjectArea.appendChild(link);
      });
    });
}

function openModal(pdfUrl) {
  document.getElementById('pdfFrame').src = pdfUrl;
  document.getElementById('pdfModal').style.display = 'block';
}

function closeModal() {
  document.getElementById('pdfModal').style.display = 'none';
  document.getElementById('pdfFrame').src = '';
}

function logout() {
  window.location.href = "/logout";
}
