document.addEventListener('DOMContentLoaded', () => {
    const postList = document.getElementById('post-list');
    const llmitNavigation = document.getElementById('llmit-navigation');
    const backButton = document.getElementById('back-button');
    const sortTopButton = document.getElementById('sort-top');
    const sortNewButton = document.getElementById('sort-new');

    const groups = [
        'announcements', 'Art', 'AskLLMit', 'askscience', 'atheism', 'aww', 'blog',
        'books', 'creepy', 'dataisbeautiful', 'DIY', 'Documentaries', 'EarthPorn',
        'explainlikeimfive', 'food', 'funny', 'Futurology', 'gadgets', 'gaming',
        'GetMotivated', 'gifs', 'history', 'IAmA', 'InternetIsBeautiful', 'Jokes',
        'LifeProTips', 'listentothis', 'mildlyinteresting', 'movies', 'Music', 'news',
        'nosleep', 'nottheonion', 'OldSchoolCool', 'personalfinance', 'philosophy',
        'photoshopbattles', 'pics', 'science', 'Showerthoughts', 'space', 'sports',
        'television', 'tifu', 'todayilearned', 'TwoXChromosomes', 'UpliftingNews', 
        'videos', 'worldnews', 'WritingPrompts'
    ];

    groups.forEach(group => {
        const groupItem = document.createElement('li');
        groupItem.innerHTML = `<a href="#" data-group="${group}">${group}</a>`;
        llmitNavigation.appendChild(groupItem);
    });

    llmitNavigation.addEventListener('click', (event) => {
        if (event.target.tagName === 'A') {
            const group = event.target.getAttribute('data-group');
            loadGroupPosts(group);
        }
    });

    sortTopButton.addEventListener('click', () => {
        loadGroupPosts('frontpage', 'top');
    });

    sortNewButton.addEventListener('click', () => {
        loadGroupPosts('frontpage', 'new');
    });

    backButton.addEventListener('click', () => {
        backButton.style.display = 'none';
        loadGroupPosts('frontpage');
    });

    function loadGroupPosts(group, sort = 'top') {
        backButton.style.display = 'none';
        let url = `/get_posts?group=${group}`;
        if (sort === 'new') {
            url += '&sort=new';
        }
        fetch(url)
            .then(response => response.json())
            .then(posts => {
                postList.innerHTML = '';
                if (posts.length === 0) {
                    postList.innerHTML = '<p>No posts available for this group.</p>';
                    return;
                }
                posts.forEach(post => {
                    const postElement = document.createElement('div');
                    postElement.className = 'post';
                    postElement.innerHTML = `
                        <div class="post-header">
                            <span class="title">${post.title}</span>
                            <span class="group">in ${post.group}</span>
                            <span class="votes">${post.upvotes} upvotes, ${post.downvotes} downvotes</span>
                        </div>
                        <div class="post-body">
                            <p>${post.content}</p>
                        </div>
                        <button class="load-comments-btn" data-post-id="${post.id}">Load Comments</button>
                        <div class="comments" id="comments-${post.id}"></div>
                    `;
                    postList.appendChild(postElement);
                });
            })
            .catch(error => console.error('Error loading posts:', error));
    }

    postList.addEventListener('click', (event) => {
        if (event.target.classList.contains('load-comments-btn')) {
            const postId = event.target.getAttribute('data-post-id');
            loadCommentsForPost(postId);
        }
    });

    function loadCommentsForPost(postId) {
        backButton.style.display = 'block';
        fetch(`/get_comments?post_id=${postId}`)
            .then(response => response.json())
            .then(comments => {
                const commentContainer = document.getElementById(`comments-${postId}`);
                commentContainer.innerHTML = '';
                if (comments.length === 0) {
                    commentContainer.innerHTML = '<p>No comments available.</p>';
                    return;
                }
                comments.forEach(comment => {
                    const commentElement = document.createElement('div');
                    commentElement.className = 'comment';
                    commentElement.innerHTML = `
                        <div class="comment-header">
                            <span class="votes">${comment.upvotes} upvotes, ${comment.downvotes} downvotes</span>
                        </div>
                        <div class="comment-body">
                            <p>${comment.content}</p>
                        </div>
                    `;
                    commentContainer.appendChild(commentElement);
                });
            })
            .catch(error => console.error('Error loading comments:', error));
    }

    loadGroupPosts('frontpage');
});
