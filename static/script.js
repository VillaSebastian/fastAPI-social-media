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
                postElement.id = post.id
                postElement.classList.add('post');
                postElement.innerHTML = `
                    <div class="post-header">
                        <h3 class="post-title">${post.title}</h3>
                        <p>Posted by: John Doe</p>
                        <button id="edit-${post.id}" class="edit-post-btn">Edit Post</button>
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
            window.editButtons = document.querySelectorAll('.edit-post-btn');
            window.editButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const postId = button.parentElement.parentElement.id

                    postElement = button.parentElement.parentElement;
                    const postTitleElement = postElement.querySelector('.post-title');
                    const postContentElement = postElement.querySelector('.post-content p');

                    // Save the original title and content
                    const originalTitle = postTitleElement.textContent;
                    const originalContent = postContentElement.textContent;

                    // Replace title and content with input fields
                    postTitleElement.innerHTML = `<input type="text" id="edit-title-${postId}" value="${originalTitle}" placeholder="${originalTitle}">`;
                    postContentElement.innerHTML = `<textarea id="edit-content-${postId}" placeholder="${originalContent}">${originalContent}</textarea>`;

                    // Add submit and cancel buttons
                    const buttonsHTML = `
                    <button id="submit-${postId}" onclick="submitEdit(${postId})">Submit</button>
                    <button id="cancel-${postId}" onclick="cancelEdit(${postId}, '${originalTitle}', '${originalContent}')">Cancel</button>
                    `;
                    postContentElement.insertAdjacentHTML('beforeend', buttonsHTML);

                    /* const updatedContent = prompt('Enter the updated content:'); // You can use a more sophisticated UI for editing
                    if (updatedContent !== null) { // User clicked "OK"
                    const updatedData = { content: updatedContent }; // Prepare the updated data
                    updatePost(postId, updatedData); // Call the updatePost function
                    } */
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

function submitEdit(postId) {
    const newTitle = document.querySelector(`#edit-title-${postId}`).value;
    const newContent = document.querySelector(`#edit-content-${postId}`).value;

    // Update the post with new values (here you should also add the logic to update the backend)
    updatedData = {
        title: newTitle,
        content: newContent
    }
    updatePost(postId, updatedData)

    // Remove submit and cancel buttons
    const submitButton = document.querySelector(`#submit-${postId}`);
    const cancelButton = document.querySelector(`#cancel-${postId}`);
    submitButton.remove();
    cancelButton.remove();
}

function cancelEdit () {
    getPosts()
}

function updatePost(postId, updatedData) {
    const updateUrl = `http://127.0.0.1:8000/posts/${postId}`;

    const fetchOptions = {
        method: 'PATCH', // Using PATCH for updating partial data
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData), // Convert the updatedData object to JSON string
    };

    fetch(updateUrl, fetchOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Parse the JSON response
        })
        .then(data => {
            console.log('Post updated successfully:', data);
            // You can perform any further actions here, such as updating the UI
            // For simplicity, you may choose to reload all posts
            getPosts();
        })
        .catch(error => {
            console.error('There was a problem with the Fetch request:', error);
        });
}