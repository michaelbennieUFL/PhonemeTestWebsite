document.addEventListener("DOMContentLoaded", function() {
    const captchaButton = document.querySelector(".btn-secondary");
    let timerInterval;

    captchaButton.addEventListener("click", function(event) {
        event.preventDefault();

        const emailInput = document.querySelector("input[name='email']");
        const usernameInput = document.querySelector("input[name='username']");
        const email = emailInput.value;
        const username = usernameInput.value;

        if (!email || !username) {
            showToast("Please enter both your email and username.", "warning");
            return;
        }

        axios.get(`/auth/captcha/email`, {
            params: {
                email: email,
                username: username
            }, 
            timeout: 90000
        })
        .then(response => {
            const data = response.data;
            if (data.code === 200) {
                showToast("Captcha sent successfully!", "success");
                startTimer();
            } else {
                showToast(data.message, "danger");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            showToast("Failed to send captcha. Please try again later.", "danger");
        });
    });

    function startTimer() {
        let countdown = 60;
        captchaButton.disabled = true;
        captchaButton.innerText = `${countdown}s`;

        timerInterval = setInterval(function() {
            countdown -= 1;
            captchaButton.innerText = `${countdown}s`;

            if (countdown <= 0) {
                clearInterval(timerInterval);
                captchaButton.disabled = false;
                captchaButton.innerText = "Resend Captcha";
            }
        }, 1000);
    }

    function showToast(message, type) {
        const toastContainer = document.createElement("div");
        toastContainer.className = `toast-container position-fixed bottom-0 end-0 p-3`;
        toastContainer.style.zIndex = 1055;

        const toast = document.createElement("div");
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute("role", "alert");
        toast.setAttribute("aria-live", "assertive");
        toast.setAttribute("aria-atomic", "true");

        const toastBody = document.createElement("div");
        toastBody.className = "toast-body fs-5";  // 增大文本大小
        toastBody.innerText = message;

        const toastCloseButton = document.createElement("button");
        toastCloseButton.className = "btn-close btn-close-white me-2 m-auto";
        toastCloseButton.setAttribute("type", "button");
        toastCloseButton.setAttribute("data-bs-dismiss", "toast");
        toastCloseButton.setAttribute("aria-label", "Close");

        toast.appendChild(toastBody);
        toast.appendChild(toastCloseButton);
        toastContainer.appendChild(toast);
        document.body.appendChild(toastContainer);

        const toastBootstrap = new bootstrap.Toast(toast);
        toastBootstrap.show();

        toast.addEventListener("hidden.bs.toast", function() {
            toastContainer.remove();
        });
    }
});
