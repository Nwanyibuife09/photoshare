import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

import Navbar from './components/Navbar';

import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import CreatorDashboard from './pages/CreatorDashboard';
import PhotoDetailPage from './pages/PhotoDetail';

import './App.css';

const ProtectedRoute = ({
  children,
  requireCreator = false,
}: {
  children: React.ReactElement;
  requireCreator?: boolean;
}) => {
  const { user, loading } = useAuth();
if (loading) return <div>Loading...</div>;

if (!user) return <Navigate to="/login" replace />;

if (requireCreator && !user.is_creator) {
  return <Navigate to="/" replace />;
}

  return children;
};

function AppRoutes() {

  const { user, loading } = useAuth();

console.log("USER:", user);
console.log("LOADING:", loading);

  return (
    <div className="app-container">
      <Navbar />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <CreatorDashboard />
              </ProtectedRoute>
            }
          />

          <Route path="/login" element={<Login />} />

          <Route path="/register" element={<Register />} />

          <Route path="/photo/:id" element={<PhotoDetailPage />} />

          <Route
            path="/creator"
            element={
              <ProtectedRoute requireCreator={true}>
                <CreatorDashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;