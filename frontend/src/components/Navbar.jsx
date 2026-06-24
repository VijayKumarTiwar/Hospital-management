import { useNavigate } from "react-router-dom";

export default function Navbar() {
    const navigate = useNavigate();

    const handleLogout = () => {
        navigate("/");
    };

    return (
        <div className="navbar" style={{ background: "#2563eb", color: "white", border: "none" }}>
            <h2 style={{ flex: 1, color: "white" }}>
                AI Healthcare
            </h2>
            <button onClick={handleLogout} style={{ background: "white", color: "#2563eb", border: "none", padding: "8px 16px", borderRadius: "6px", cursor: "pointer", fontWeight: "bold" }}>
                Logout
            </button>
        </div>
    );
}