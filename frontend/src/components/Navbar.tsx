import { Link, useNavigate } from 'react-router-dom';
import { Camera } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <Camera size={28} className="brand-icon"/>
          <span>PhotoShare</span>
        </Link>
        <div className="navbar-links">
          {user ? (
            <>
              {user.is_creator && (
  <>
    <Link to="/creator" className="nav-link btn-secondary">
      Creator Dashboard
    </Link>

    <Link to="/creator" className="nav-link btn-primary">
      Upload Image
    </Link>
  </>
)}
              <span className="nav-text">Hi, {user.username}</span>
              <button onClick={handleLogout} className="btn-outline">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="nav-link btn-primary">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
