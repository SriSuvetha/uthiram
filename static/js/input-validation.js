const re = {
    name: /^[a-z\.]*$/i,
    age: /^[\d]{0,3}$/,
    mobile: /^[\d]{10,10}$/,
    pincode: /^[\d]{6,6}$/,
    email: /^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$/gi,
    password: /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8})/g
}

const isAllValid = {};
const requiredField = {
    field: new Set(),
    total: 0
};

const checkRequiredFieldFilled = (e) => {
    e.target.value === "" ? requiredField.field.delete(e.target) : requiredField.field.add(e.target);
    console.log(requiredField.field.size);
}

const validate = (e) => {
    const val = e.target.value;
    const tagName = e.target.name;
    const reName = e.target.dataset.re;
    const errTag = e.target.parentElement.querySelector(`.form--input-err`);
    if(val === ""){
        isAllValid[tagName] = false;
    }
    else{
        isAllValid[tagName] = val.match(re[reName]) ? true : false;
    }
    toggleError(errTag, e.target, isAllValid[tagName]);
}

const toggleError = (errTag, inputTag, isValid) => {
    if(!isValid){
        errTag .innerText = inputTag.dataset.msg;
        inputTag.classList.add("invalid");
    }
    else{
        errTag .innerText = "";
        inputTag.classList.remove("invalid");
    }
}

const checkAllValid = () => Object.values(isAllValid).every(validity => validity);

const submitForm = (e) => {
    e.preventDefault();
    if(checkAllValid() && requiredField.total == requiredField.field.size){
        console.log(true);
        //TODO: Add subimission redirects
    }
    else{
        console.log(false);
        e.target.classList.add("form--button-err");
        setTimeout(() => {e.target.classList.remove("form--button-err")}, 2000);
    }
}

const inputTag = document.querySelectorAll(".form--input-value");
const submitButton = document.querySelector(".form--button-submit");
inputTag.forEach(tag => {
    if(tag.required){
        requiredField.total++;
        tag.addEventListener("input", checkRequiredFieldFilled);
    }
    if(!tag.dataset.re) return;
    const tagName = tag.name;
    isAllValid[tagName] = false;
    tag.addEventListener("input", validate);
});

submitButton.addEventListener("click", submitForm);