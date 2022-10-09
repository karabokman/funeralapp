const usernameField=document.querySelector('#usernamefield');
const feedBackArea=document.querySelector('.invalid_feedback');
const emailField=document.querySelector('#emailfield');
const emailfeedBackArea=document.querySelector('.emailinvalid_feedback');
const showPasswordToggle=document.querySelector('.showPasswordToggle')
const passwordField=document.querySelector('#passwordfield');
const submitBtn=document.querySelector('.submit-btn');


const handleToggleInput=(e)=>{

    if (showPasswordToggle.textContent=='SHOW'){
        showPasswordToggle.textContent='HIDE';
        passwordField.setAttribute("type", "text");
    }else{
        showPasswordToggle.textContent='SHOW';
        passwordField.setAttribute("type", "password");
    }

};

showPasswordToggle.addEventListener("click", handleToggleInput);

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    console.log("emailVal", emailVal);

    emailField.classList.remove("is-invalid");
    emailfeedBackArea.style.display="none";

    if (emailVal.length > 0){
        fetch("/authentication/validate-email", {
        body:JSON.stringify({email: emailVal}),
        method: "POST",
        }).then(res=>res.json()).then(data=>{
        console.log("data", data);
        if (data.email_error) {
            submitBtn.disabled=true;
            emailField.classList.add("is-invalid");
            emailfeedBackArea.style.display="block";
            emailfeedBackArea.innerHTML= data.email_error;
            console.log("data", data.email_error);
            }else{
            submitBtn.removeAttribute('disabled');
                }
        });
        }
});

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    console.log("usernameVal", usernameVal);

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display="none";


    if (usernameVal.length > 0){
        fetch("/authentication/validate-username", {
        body:JSON.stringify({username: usernameVal}),
        method: "POST",
        }).then(res=>res.json()).then(data=>{
        console.log("data", data);
        if (data.username_error) {
            submitBtn.disabled=true;
            usernameField.classList.add("is-invalid");
            feedBackArea.style.display="block";
            feedBackArea.innerHTML= data.username_error;
            console.log("data", data.username_error);
            }else{
            submitBtn.removeAttribute('disabled');
                }
        });
        }
});