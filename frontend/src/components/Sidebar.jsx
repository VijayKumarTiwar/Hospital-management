import { Link } from "react-router-dom";

export default function Sidebar() {
    return (
        <div className="sidebar glass-panel" style={{ borderTop: "none", borderBottom: "none", borderLeft: "none", borderRadius: "0" }}>
            <h3 style={{ marginTop: "10px" }}>Menu</h3>
            <Link to="/dashboard" className="sidebar-link">Dashboard</Link>
            <Link to="/accounts" className="sidebar-link">Accounts</Link>
            <Link to="/patients" className="sidebar-link">Patients</Link>
            <Link to="/doctors" className="sidebar-link">Doctors</Link>
            <Link to="/appointments" className="sidebar-link">Appointments</Link>
            <Link to="/chatbot" className="sidebar-link">Chatbot</Link>
            <Link to="/notifications" className="sidebar-link">Notifications</Link>
            <Link to="/prediction" className="sidebar-link">Prediction</Link>
            <Link to="/reminders" className="sidebar-link">Reminders</Link>
            <Link to="/reports" className="sidebar-link">Reports</Link>
        </div>
    );
}