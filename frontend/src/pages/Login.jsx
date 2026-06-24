import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import PersonIcon from "@mui/icons-material/Person";
import LockIcon from "@mui/icons-material/Lock";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import api from "../services/api";
import { useAuth } from "../services/authContext";
import "./Login.css";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [rememberMe, setRememberMe] = useState(false);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const { login: loginUser } = useAuth();

    const login = async (e) => {
        e.preventDefault();
        if (!email || !password) {
            toast.warning("Please enter both email and password.");
            return;
        }
        setLoading(true);
        try {
            const res = await api.post("accounts/login/", { email, password });
            
            // Assuming the backend returns { access, refresh, user: {...} } or similar.
            // If backend only returns tokens, we might need a separate profile fetch,
            // but our authContext initAuth will do that if we set tokens and reload or wait.
            // Let's set tokens and fetch profile immediately.
            const { access, refresh } = res.data.tokens;

            
            // Temporary set until authContext handles the profile load:
            loginUser(null, access, refresh);
            
            // Fetch profile right away so we have user details
            const profileRes = await api.get('accounts/profile/', {
                headers: { Authorization: `Bearer ${access}` }
            });
            loginUser(profileRes.data, access, refresh);

            toast.success("Login successful!");
            navigate("/dashboard");
        } catch (error) {
            console.error(error);
            toast.error("Login failed. Please check your credentials.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page-bg">
            <div className="login-card-gradient">
                <div className="login-logo-container">
                    {/* Placeholder for the logo */}
                    <div className="logo-placeholder" style={{ borderRadius: "50%" }}>
                        <LocalHospitalIcon style={{ color: "#ed1c24", fontSize: "40px" }} />
                    </div>
                </div>
                
                <h1 className="welcome-text">WELCOME!</h1>
                <h2 className="subtitle-text">HOSPITAL</h2>

                <form onSubmit={login} className="login-form">
                    <div className="custom-input-group">
                        <PersonIcon className="input-icon" />
                        <input
                            type="text"
                            placeholder="admin@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>

                    <div className="custom-input-group">
                        <LockIcon className="input-icon" />
                        <input
                            type="password"
                            placeholder="........."
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    <div className="remember-me-group">
                        <input 
                            type="checkbox" 
                            id="remember" 
                            checked={rememberMe}
                            onChange={(e) => setRememberMe(e.target.checked)}
                        />
                        <label htmlFor="remember">Remember me?</label>
                    </div>

                    <div className="submit-group">
                        <button type="submit" className="login-btn" disabled={loading}>
                            {loading ? "Logging in..." : "Log in"}
                        </button>
                    </div>
                </form>

                <div className="login-footer">
                    DESIGNED & DEVELOPED BY <span className="highlight-company">Vjay Software PVT Ltd</span>.
                </div>
            </div>
        </div>
    );
}