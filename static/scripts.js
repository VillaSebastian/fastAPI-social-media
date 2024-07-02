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
                window.location.pathname = '/view/posts'
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

    const postForm = document.getElementById('post-form');
    if (postForm) {
        postForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(event.target);
            const title = formData.get('input-title');
            const content = formData.get('input-content');
            const token = window.sessionStorage.getItem('accessToken');

            if (confirm("Do you really want to submit this post?")) {
                try {
                    const response = await fetch('http://127.0.0.1:8000/posts', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({title, content})
                    });
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail);
                    }
                    const data = await response.json();
                    console.log('Post created successfully:', data);
                    location.reload();
                } catch (error) {
                    console.error('Could not create post:', error.message);
                    // Display error message to the user
                    const errorMessageElement = document.getElementById('error-message');
                    if (errorMessageElement) {
                        errorMessageElement.textContent = error.message;
                        errorMessageElement.style.display = 'block';
                    }
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
                const postLink = document.createElement('a');
                postLink.classList.add('clickable-post');
                postLink.setAttribute('href', `http://127.0.0.1:8000/view/posts/${post.id}`);

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
                postLink.appendChild(postElement);
                postsContainer.appendChild(postLink);
            });
        })
    }

    const singlePostContainer = document.getElementById('single-post-container');
    if (singlePostContainer) {
        var postId = window.location.pathname.split('/')[3];
        fetch(`http://127.0.0.1:8000/posts/${postId}`)
        .then(response => post = response.json())
        .then(post => {
            singlePostContainer.innerHTML = `
            <div class="post-header">
                <!-- <img src="profile-pic.jpg" alt="Profile Picture" class="profile-pic"> -->
                <span class="username">Posted by: ${post.user_id}</span>
                <button id="edit-button" style="display: none;">Edit Post</button>
                <button id="delete-button" style="display: none;">Delete Post</button>
            </div>
            <div class="post-title">${post.title}</div>
            <div class="post-content">${post.content}</div>
            <div class="post-footer">
                <!-- <span class="user-id">User ID: ${post.user_id}</span> -->
                <span class="created-at">Created at: ${post.created_at}</span>
            </div>
            `;
            const token = window.sessionStorage.getItem('accessToken');
            const currentUserId = jwt_decode(token).user_id;
            if (currentUserId === post.user_id) {
                document.getElementById('edit-button').style.display = 'block';
            }
            document.getElementById('edit-button').addEventListener('click', () => {
                enableEditMode(post);
            });

            document.getElementById('delete-button').addEventListener('click', () => {
                deletePost(postId);
            });
        })
    }
});

function enableEditMode(post) {
    const postTitle = document.querySelector('.post-title');
    const postContent = document.querySelector('.post-content');
    const editButton = document.getElementById('edit-button');
    const deleteButton = document.getElementById('delete-button');

    postTitle.innerHTML = `<input type="text" id="title-input" value="${post.title}">`;
    postContent.innerHTML = `<textarea id="content-input">${post.content}</textarea>`;

    editButton.textContent = 'Save Changes';
    editButton.removeEventListener('click', enableEditMode);
    editButton.addEventListener('click', () => saveChanges(post.id));

    deleteButton.style.display = 'block';
}

function saveChanges(postId) {
    console.log('Function saveChanges called with postId:', postId); // Debugging
    const updatedTitle = document.getElementById('title-input').value;
    const updatedContent = document.getElementById('content-input').value;
    console.log('Updated Title:', updatedTitle); // Debugging
    console.log('Updated Content:', updatedContent); // Debugging
    debugger;

    fetch(`http://127.0.0.1:8000/posts/${postId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${window.sessionStorage.getItem('accessToken')}`
        },
        body: JSON.stringify({
            title: updatedTitle,
            content: updatedContent
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(post => {
        document.querySelector('.post-title').innerText = post.title;
        document.querySelector('.post-content').innerText = post.content;
        document.getElementById('edit-button').textContent = 'Edit Post';
        document.getElementById('delete-button').style.display = 'none';
    })
    .catch(error => console.error('Error:', error));
}

function deletePost(postId) {
    fetch(`http://127.0.0.1:8000/posts/${postId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${window.sessionStorage.getItem('accessToken')}`
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/'; // Redirect to home page after deletion
        } else {
            console.error('Failed to delete post');
        }
    })
    .catch(error => console.error('Error:', error));
}