import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <a className="navbar-brand" href="/">Gym System</a>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <a className="nav-link" href="/schedules">Schedules</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/blog">Blog</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
