document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.querySelector("form");

    // Khi form được gửi
    loginForm.addEventListener("submit", function(event) {
        // Không cần ngừng gửi form nữa vì chúng ta sử dụng form mặc định
        // event.preventDefault();

        // Kiểm tra nếu có thiếu thông tin
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        if (!username || !password) {
            alert("Please fill out all fields.");
            return;
        }
    });
});
