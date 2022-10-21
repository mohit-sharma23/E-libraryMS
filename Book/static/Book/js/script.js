const container = document.querySelector(".container"),
      pwShowHide = document.querySelector(".showHidePw"),
      pwFields = document.querySelector("#mera"),
      signUp = document.querySelector(".signup-link"),
      login = document.querySelector(".login-link");
console.log("helsx")
console.log("jjjj")
    //   js code to show/hide password and change icon
    pwShowHide.addEventListener('click', ()=>{
        if(pwFields.type==="password"){
            console.log("qqqq");
            pwFields.type="text";
            pwShowHide.classList.remove('uil-eye-slash')
            pwShowHide.classList.add('uil-eye')
            // pwShowHide(icon =>{
            //     icon.classList.replace("uil-eye-slash", "uil-eye");
            // })
        }
        else{
            pwFields.type="password";
            pwShowHide.classList.remove('uil-eye')
            pwShowHide.classList.add('uil-eye-slash')
        }
    })


    // pwShowHide.forEach(eyeIcon =>{
    //     eyeIcon.addEventListener("click", ()=>{
    //         pwFields.forEach(pwField =>{
    //             if(pwField.type ==="password"){
    //                 console.log("llll")
    //                 pwField.type = "text";

    //                 pwShowHide.forEach(icon =>{
    //                     icon.classList.replace("uil-eye-slash", "uil-eye");
    //                 })
    //             }else{
    //                 pwField.type = "password";

    //                 pwShowHide.forEach(icon =>{
    //                     icon.classList.replace("uil-eye", "uil-eye-slash");
    //                 })
    //             }
    //         }) 
    //     })
    // })


    // js code to appear signup and login form
    signUp.addEventListener("click", ( )=>{
        container.classList.add("active");
    });
    login.addEventListener("click", ( )=>{
        container.classList.remove("active");
    });
