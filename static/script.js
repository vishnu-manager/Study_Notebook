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
        const section = document.createElement("div");
        section.innerHTML = `<h3>${year}</h3>`;

        const ul = document.createElement("ul");

        years[year].forEach(subject => {
            const li = document.createElement("li");
            li.style.cursor = "pointer";
            li.style.color = "blue";
            li.textContent = subject;
            li.onclick = function () {
                const subjectPDF = `/static/notes/${branch}/${year}/${subject}.pdf`;
                fetch(subjectPDF)
                    .then(response => {
                        if (response.ok) {
                            document.getElementById("pdfViewer").innerHTML =
                                `<iframe src="${subjectPDF}" width="100%" height="600px"></iframe>`;
                        } else {
                            document.getElementById("pdfViewer").innerHTML =
                                `<p style="color:red;">PDF for <b>${subject}</b> is not available right now.</p>`;
                        }
                    })
                    .catch(error => {
                        document.getElementById("pdfViewer").innerHTML =
                            `<p style="color:red;">Error loading <b>${subject}</b>: ${error}</p>`;
                    });
            };
            ul.appendChild(li);
        });

        section.appendChild(ul);
        container.appendChild(section);
    }
}
