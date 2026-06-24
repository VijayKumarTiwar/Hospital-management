import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import api from "../services/api";

export default function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const register = async (e) => {
        e.preventDefault();
        if (!name || !email || !password) {
            toast.warning("Please fill in all fields.");
            return;
        }
        setLoading(true);
        try {
            await api.post("accounts/register/", { username: name, email, password });
            toast.success("Registration successful! Please login.");
            navigate("/");
        } catch (error) {
            console.error(error);
            toast.error("Registration failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card glass-panel">
                <h2>Create Account</h2>
                <p style={{ textAlign: "center", color: "var(--text-muted)", marginBottom: "10px" }}>
                    Join AI Healthcare today
                </p>
                <form onSubmit={register} style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
                    <div className="input-group">
                        <input
                            type="text"
                            placeholder="Full Name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                    <div className="input-group">
                        <input
                            type="email"
                            placeholder="Email Address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="input-group">
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button type="submit" className="btn-primary" disabled={loading}>
                        {loading ? "Registering..." : "Register"}
                    </button>
                </form>
                <Link to="/" className="link-text">
                    Already have an account? Login here
                </Link>
            </div>
        </div>
    );
}