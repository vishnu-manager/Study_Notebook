<script>
function showSubjects(branch) {
    const subjectsByYear = {
        CSE: {
            "1st Year": ["Maths I", "Physics", "C Programming", "Engineering Drawing"],
            "2nd Year": ["DSA", "OOPs", "DBMS", "Digital Logic"],
            "3rd Year": ["OS", "CN", "AI", "ML"],
            "4th Year": ["Big Data", "Cloud Computing", "Blockchain"]
        },
        CIVIL: {
            "1st Year": ["Engineering Mechanics", "Surveying", "Construction Materials"],
            "2nd Year": ["Structural Analysis", "Fluid Mechanics"],
            "3rd Year": ["Transportation", "Concrete Design"],
            "4th Year": ["Estimation", "Advanced Structures"]
        },
        MECH: {
            "1st Year": ["Engineering Graphics", "Thermodynamics"],
            "2nd Year": ["Mechanics of Solids", "Fluid Mechanics"],
            "3rd Year": ["Machine Design", "Heat Transfer"],
            "4th Year": ["Robotics", "CAD/CAM"]
        },
        EEE: {
            "1st Year": ["Basic Electrical", "Circuit Theory"],
            "2nd Year": ["Electrical Machines", "Electromagnetic Fields"],
            "3rd Year": ["Control Systems", "Power Electronics"],
            "4th Year": ["Smart Grids", "Renewable Energy"]
        }
    };

    const container = document.getElementById("subjectContainer");
    container.innerHTML = `<h2>${branch} Subjects</h2>`;
    
    const years = subjectsByYear[branch];

    for (let year in years) {
        const yearSection = document.createElement("div");
        yearSection.className = "year-section";
        yearSection.innerHTML = `<h3>${year}</h3>`;

        const ul = document.createElement("ul");
        ul.className = "subject-list";

        years[year].forEach(subject => {
            const li = document.createElement("li");
            li.textContent = subject;
            li.className = "subject-item";

            li.onclick = function () {
                const encodedSubject = encodeURIComponent(subject);
                const pdfURL = `/static/notes/${branch}/${year}/${encodedSubject}.pdf`;

                fetch(pdfURL)
                    .then(response => {
                        if (response.ok) {
                            document.getElementById("pdfViewer").innerHTML = `
                                <iframe src="${pdfURL}" width="100%" height="600px" frameborder="0"></iframe>`;
                        } else {
                            document.getElementById("pdfViewer").innerHTML = `
                                <p class="error-text">PDF for <b>${subject}</b> is not available.</p>`;
                        }
                    })
                    .catch(err => {
                        document.getElementById("pdfViewer").innerHTML = `
                            <p class="error-text">Error loading <b>${subject}</b>: ${err}</p>`;
                    });
            };

            ul.appendChild(li);
        });

        yearSection.appendChild(ul);
        container.appendChild(yearSection);
    }
}
</script>
