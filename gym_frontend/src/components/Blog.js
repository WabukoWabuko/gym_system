import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Blog = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/blogposts/')
      .then(response => setPosts(response.data))
      .catch(error => console.error('Error fetching posts:', error));
  }, []);

  return (
    <div className="container mt-4">
      <h2>Blog</h2>
      {posts.map(post => (
        <div key={post.id} className="card mb-3">
          <div className="card-body">
            <h5 className="card-title">{post.title}</h5>
            <p className="card-text">{post.content}</p>
            <p className="text-muted">{new Date(post.pub_date).toLocaleDateString()}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Blog;
