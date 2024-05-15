const postUrl = 'http://127.0.0.1:8000/posts';
const inputTitle = document.getElementById('input-title');
const inputContent = document.getElementById('input-content');
const createPostButton = document.getElementById('create-post-button');
const postForm = document.getElementById('post-form');
const postList = document.getElementById('post-list');
// const postDiv = document.querySelector(".post")

document.addEventListener("DOMContentLoaded", getPosts)
postForm.addEventListener('submit', createPost);


function getPosts() {
    const postUrl = 'http://127.0.0.1:8000/posts';
    fetch(postUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Parse the JSON response
        })
        .then(posts => {
            postList.innerHTML = '';

            posts.data.forEach(post => {
                const postElement = document.createElement('div');
                postElement.classList.add('post');
                postElement.innerHTML = `
                    <div class="post-header">
                        <h3 class="post-title">${post.title}</h3>
                        <p>Posted by: John Doe</p>
                    </div>

                    <div class="post-content">
                        <p>${post.content}</p>
                        <p>Post: <span>${post.id}</span></p>
                        <button id="${post.id}" class="delete-post-btn">Delete Post</button>
                    </div>
                `;
                postList.appendChild(postElement);
            })
            window.deleteButtons = document.querySelectorAll('.delete-post-btn');
            window.deleteButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const postId = button.id;
                    deletePost(postId);
                });
            }); 
        })
        .catch(error => {
            console.error('There was a problem with the Fetch request:', error);
        })
}

function createPost(event) {

    if (event) {
        event.preventDefault();
    } else {
        return false;
    }

    const postUrl = 'http://127.0.0.1:8000/posts';    
    const postData = {
    title: inputTitle.value,
    content: inputContent.value
    // Add any other relevant data for your social media post
    };

    // Define the configuration for the Fetch request
    const fetchOptions = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        // Add any other required headers, such as authentication tokens
    },
    body: JSON.stringify(postData), // Convert the postData object to JSON string
    };

    // Make the Fetch request
    fetch(postUrl, fetchOptions)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        // Handle the response data
        console.log('Post created successfully:', data);
        // You can perform any further actions here, such as updating the UI
        const postElement = document.createElement('div');
        postElement.classList.add('post');
        postElement.innerHTML = `
        <h3>${postData.title}</h3>
        <p>${postData.content}</p>
        `;
        postList.appendChild(postElement);
        getPosts()
    })
    .catch(error => {
        // Handle any errors that occur during the Fetch request
        console.error('There was a problem with the Fetch request:', error);
    });
}

function deletePost(postId) {
    const deleteUrl = `http://127.0.0.1:8000/posts/${postId}`;

    const fetchOptions = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    };

    fetch(deleteUrl, fetchOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Parse the JSON response
        })
        .then(data => {
            console.log('Post deleted successfully:', data);
            // Remove the deleted post from the UI
            const postElement = document.getElementById(postId);
            if (postElement) {
                postElement.parentElement.remove(); // Remove the post's parent element
            }
            getPosts()
        })
        .catch(error => {
            console.error('There was a problem with the Fetch request:', error);
        });
}