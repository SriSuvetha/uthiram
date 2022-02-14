const formBloodType = document.querySelector(".form--blood-type");
const formPveBtn = document.querySelector(".form--button-positive");
const formNveBtn = document.querySelector(".form--button-negative");


formNveBtn.addEventListener("click", ()=> {
    formBloodType.setAttribute("value","negative");
    formNveBtn.style.backgroundColor = "#f00";
    formNveBtn.style.color="#fff";
    formPveBtn.style.backgroundColor = "#fff";
    formPveBtn.style.color="#746868";
});

formPveBtn.addEventListener("click", ()=> {
    formBloodType.setAttribute("value","positive");
    formPveBtn.style.backgroundColor = "#f00";
    formPveBtn.style.color="#fff";
    formNveBtn.style.backgroundColor = "#fff";
    formNveBtn.style.color="#746868";
});
