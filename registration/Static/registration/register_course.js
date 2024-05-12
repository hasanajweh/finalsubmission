document.addEventListener('DOMContentLoaded', function() {
    const registerButtons = document.querySelectorAll('.register-course-btn');

    registerButtons.forEach(button => {
        button.addEventListener('click', function() {
            const courseId = this.dataset.courseId;
            fetch(`/registration/course/${courseId}/register/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Function to get CSRF token from cookies
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'course_id': courseId })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if(data.success) {
                    window.location.reload(); // Reload the page to update the schedule or any other content
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
