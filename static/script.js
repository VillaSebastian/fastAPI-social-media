const postUrl = 'http://127.0.0.1:8000/posts';
const inputTitle = document.getElementById('input-title');
const inputContent = document.getElementById('input-content');
const createPostButton = document.getElementById('create-post-button');
const postForm = document.getElementById('post-form');
const postList = document.getElementById('post-list');

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
                    <h3>${post.title}</h3>
                    <p>${post.content}</p>
                `;
                postList.appendChild(postElement);
            })
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
    })
    .catch(error => {
        // Handle any errors that occur during the Fetch request
        console.error('There was a problem with the Fetch request:', error);
    });

    const postElement = document.createElement('div');
    postElement.classList.add('post');
    postElement.innerHTML = `
        <h3>${postData.title}</h3>
        <p>${postData.content}</p>
    `;
    postList.appendChild(postElement);

    getPosts()
}