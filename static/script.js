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
            const postList = document.getElementById('post-list');
            postList.innerHTML = '';

            posts.data.forEach(post => {
                const postElement = document.createElement('div');
                postElement.classList.add('post');
                postElement.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                `;
                postList.appendChild(postElement);
            })
        })
        .catch(error => {
            console.error('There was a problem with the Fetch request:', error);
        }

        )
}

getPosts()