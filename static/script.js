// /static/script.js

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

function showSubjects(branch) {
  const subjectArea = document.getElementById('subjectArea');
  subjectArea.innerHTML = `<h2>${branch} Subjects</h2>`;

  const subjects = subjectsByBranch[branch];
  for (const year in subjects) {
    const yearDiv = document.createElement("div");
    yearDiv.innerHTML = `<h3 class='year-title'>${year}</h3>`;
    const listDiv = document.createElement("div");
    listDiv.classList.add("subject-list");

    subjects[year].forEach(subject => {
      const subDiv = document.createElement("div");
      subDiv.classList.add("subject-item");
      subDiv.innerText = subject;
      subDiv.onclick = () => openPDF(branch, year, subject);
      listDiv.appendChild(subDiv);
    });

    yearDiv.appendChild(listDiv);
    subjectArea.appendChild(yearDiv);
  }
}

function openPDF(branch, year, subject) {
  // Clean filename
  const fileName = `${branch}_${year}_${subject}`.replace(/\s+/g, '_') + `.pdf`;
  const filePath = `/static/pdfs/${fileName}`;

  const modal = document.getElementById("popupModal");
  const pdfFrame = document.getElementById("pdfFrame");
  pdfFrame.src = filePath;
  modal.style.display = "block";
}

function closeModal() {
  const modal = document.getElementById("popupModal");
  const pdfFrame = document.getElementById("pdfFrame");
  modal.style.display = "none";
  pdfFrame.src = "";
}
