document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = event.target.email.value;
            const password = event.target.password.value;

            try {
                const response = await fetch('http://127.0.0.1:8000/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({email, password})
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail);
                }
                const data = await response.json();
                console.log('User created successfully:', data);
            } catch (error) {
                console.error('Could not create user:', error.message);
                // Display error message to the user
                const errorMessageElement = document.getElementById('error-message');
                if (errorMessageElement) {
                    errorMessageElement.textContent = error.message;
                    errorMessageElement.style.display = 'block';
                }
            }
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const username = event.target.email.value;
            const password = event.target.password.value;

            const formData = new FormData();
            formData.append('grant_type', 'password');
            formData.append('username', username);
            formData.append('password', password);

            try {
                const response = await fetch('http://127.0.0.1:8000/login', {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail);
                }
                const data = await response.json();
                sessionStorage.setItem('accessToken', data.access_token);
                window.location.href = data.url;
            } catch (error) {
                console.error('Could not login user:', error.message);
                // Display error message to the user
                const errorMessageElement = document.getElementById('error-message');
                if (errorMessageElement) {
                    errorMessageElement.textContent = error.message;
                    errorMessageElement.style.display = 'block';
                }
            }
        });
    }

    const postsContainer = document.getElementById('posts-container');
    if (postsContainer) {
        fetch('http://127.0.0.1:8000/posts')
        .then(response => response.json())
        .then(posts => {
            posts.forEach(post => {
                const postElement = document.createElement('div');
                postElement.classList.add('post');
                postElement.innerHTML = `
                <div class="post-header">
                    <!-- <img src="profile-pic.jpg" alt="Profile Picture" class="profile-pic"> -->
                    <span class="username">Posted by: ${post.user_id}</span>
                </div>
                <div class="post-title">${post.title}</div>
                <div class="post-content">${post.content}</div>
                <div class="post-footer">
                    <!-- <span class="user-id">User ID: ${post.user_id}</span> -->
                    <span class="created-at">Created at: ${post.created_at}</span>
                </div>
                `;
                postsContainer.appendChild(postElement);
            });
        })
    }
});