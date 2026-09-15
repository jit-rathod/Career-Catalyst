// ===== Auto-hide flash messages =====
setTimeout(() => {
    document.querySelectorAll(".flash").forEach(f => {
        f.style.opacity = "0";
        f.style.transform = "translateX(20px)";
        f.style.transition = "all 0.4s ease";
        setTimeout(() => f.remove(), 400);
    });
}, 3500);


// ===== Show/hide CGPA based on role =====
const roleField = document.querySelector('[name="role"]');
const cgpaField = document.getElementById("cgpa-field");

if (roleField && cgpaField) {
    function toggleCGPA() {
        cgpaField.style.display = roleField.value === "admin" ? "none" : "block";
    }
    roleField.addEventListener("change", toggleCGPA);
    toggleCGPA();
}


// ===== Render star ratings =====
document.querySelectorAll(".star-rating[data-rating]").forEach(el => {
    const rating = parseFloat(el.dataset.rating) || 0;
    let html = "";
    for (let i = 1; i <= 5; i++) {
        if (i <= Math.floor(rating)) {
            html += '<span class="star filled">★</span>';
        } else if (i === Math.ceil(rating) && rating % 1 >= 0.5) {
            html += '<span class="star partial">★</span>';
        } else {
            html += '<span class="star empty">☆</span>';
        }
    }
    el.innerHTML = html;
});


// ===== CGPA bar animation =====
document.querySelectorAll(".cgpa-bar").forEach(bar => {
    const pct = parseFloat(bar.dataset.pct) || 0;
    bar.style.width = "0%";
    setTimeout(() => { bar.style.width = pct + "%"; }, 200);
});


// ===== Hamburger menu (mobile) =====
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');
if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('open');
        navLinks.classList.toggle('open');
    });
    // Close menu when a link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('open');
            navLinks.classList.remove('open');
        });
    });
}
