document.addEventListener('DOMContentLoaded', () => {
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');

    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });

    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });
});

let eye = document.getElementById("eye");
eye.addEventListener('click', function () {
     if (this.previousElementSibling.getAttribute('type') == 'password') {
          this.previousElementSibling.setAttribute('type', 'text');
          this.classList.toggle('fa-eye');
          this.classList.toggle('fa-eye-slash');
     } else {
          this.previousElementSibling.setAttribute('type', 'password');
          this.classList.toggle('fa-eye');
          this.classList.toggle('fa-eye-slash');
     }
})


let eye2 = document.getElementById("eye2");
eye2.addEventListener('click', function () {
     if (this.previousElementSibling.getAttribute('type') == 'password') {
          this.previousElementSibling.setAttribute('type', 'text');
          this.classList.toggle('fa-eye');
          this.classList.toggle('fa-eye-slash');
     } else {
          this.previousElementSibling.setAttribute('type', 'password');
          this.classList.toggle('fa-eye');
          this.classList.toggle('fa-eye-slash');
     }
})


let eye3 = document.getElementById("eye3");
eye3.addEventListener('click', function () {
     if (this.previousElementSibling.getAttribute('type') == 'password') {
          this.previousElementSibling.setAttribute('type', 'text');
          this.classList.toggle('fa-eye');
          this.classList.toggle('fa-eye-slash');
     } else {
          this.previousElementSibling.setAttribute('type', 'password');
          this.classList.toggle('fa-eye');
          this.classList.toggle('fa-eye-slash');
     }
})
