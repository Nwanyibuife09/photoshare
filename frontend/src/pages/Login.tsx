import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { login} = useAuth();

 const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault();
  setLoading(true);

  try {
    const data = new URLSearchParams();
    data.append("username", username);
    data.append("password", password);

    const response = await api.post("/auth/login", data, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    // 1. save token
    localStorage.setItem("token", response.data.access_token);

    // 2. fetch real user (THIS IS THE FIX)
    const me = await api.get("/auth/me");

    // 3. set auth user properly
    login(response.data.access_token, me.data);

    navigate("/dashboard");

  } catch (error: any) {
    console.log("LOGIN ERROR:", error.response?.data || error.message);
    alert("Login failed");
  } finally {
    setLoading(false);
  }
};

  return (
    <div style={{ maxWidth: "400px", margin: "100px auto" }}>
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <br /><br />

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>

      <p>
        Don’t have an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}