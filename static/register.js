document.addEventListener('DOMContentLoaded', () => {
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');

    // 初期状態でSign Up画面を表示
    container.classList.add("right-panel-active");

    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });

    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });
});


