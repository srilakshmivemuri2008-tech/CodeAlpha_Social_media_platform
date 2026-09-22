// Handles the like and follow buttons via fetch(), so the page never reloads.

document.addEventListener('click', async function (e) {
    // --- LIKE BUTTON ---
    const likeBtn = e.target.closest('.like-btn');
    if (likeBtn) {
        const postId = likeBtn.dataset.postId;
        try {
            const res = await fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.CSRF_TOKEN,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
            if (!res.ok) throw new Error('Request failed');
            const data = await res.json();

            likeBtn.dataset.liked = data.liked ? 'true' : 'false';
            likeBtn.classList.toggle('liked', data.liked);
            likeBtn.querySelector('.like-icon').textContent = data.liked ? '❤️' : '🤍';
            likeBtn.querySelector('.like-count').textContent = data.like_count;
        } catch (err) {
            console.error('Like failed:', err);
        }
        return;
    }

    // --- FOLLOW BUTTON ---
    const followBtn = e.target.closest('.follow-btn');
    if (followBtn) {
        const username = followBtn.dataset.username;
        try {
            const res = await fetch(`/u/${username}/follow/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.CSRF_TOKEN,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
            if (!res.ok) throw new Error('Request failed');
            const data = await res.json();

            followBtn.dataset.following = data.following ? 'true' : 'false';
            followBtn.textContent = data.following ? 'Unfollow' : 'Follow';
        } catch (err) {
            console.error('Follow failed:', err);
        }
        return;
    }
});
