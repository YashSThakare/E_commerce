
let slideIndex = 0;
showSlides();

function showSlides() {
    let slides = document.getElementsByClassName("b02-1-pXo");
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }
    slides[slideIndex - 1].style.display = "block";
    setTimeout(showSlides, 2000); // Change image every 3 seconds (adjust this as desired)
}


