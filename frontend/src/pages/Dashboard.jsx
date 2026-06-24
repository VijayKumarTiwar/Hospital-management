import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";
import { useAuth } from "../services/authContext";

export default function Dashboard() {
    const { user } = useAuth();
    const [appointments, setAppointments] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [overviewData, setOverviewData] = useState(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            if (!user) return;
            try {
                // Fetch Appointments
                const appRes = await api.get("appointments/");
                setAppointments(appRes.data || []);

                // Fetch Notifications count
                // Assume the endpoint returns an array and we count it, or it returns {count: X}
                const notifRes = await api.get("notifications/unread-count/");
                setUnreadCount(notifRes.data?.length || notifRes.data?.count || 0);

                // Fetch Role specific overview
                if (user.role === 'patient') {
                    const overRes = await api.get("dashboard/patient/");
                    setOverviewData(overRes.data);
                } else if (user.role === 'doctor') {
                    const overRes = await api.get("dashboard/doctor/");
                    setOverviewData(overRes.data);
                } else if (user.role === 'admin') {
                    const overRes = await api.get("dashboard/admin/");
                    setOverviewData(overRes.data);
                }
            } catch (err) {
                console.error("Error fetching dashboard data", err);
            }
        };

        fetchDashboardData();
    }, [user]);

    return (
        <div className="app-layout">
            <Sidebar />
            <div className="main-content">
                <Navbar />
                <div className="dashboard-content">
                    <h1>Welcome, {user?.first_name || user?.username || 'User'}!</h1>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "20px" }}>
                        <div className="glass-panel" style={{ padding: "30px" }}>
                            <h3>Upcoming Appointments</h3>
                            {appointments.length > 0 ? (
                                <ul style={{ marginTop: "10px", color: "var(--text-muted)", listStyle: "none", padding: 0 }}>
                                    {appointments.slice(0, 3).map(app => (
                                        <li key={app.id} style={{ marginBottom: "5px" }}>
                                            {app.scheduled_at.split('T')[0]} - {user?.role === 'patient' ? `Dr. ${app.doctor_name}` : app.patient_name}
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p style={{ marginTop: "10px", color: "var(--text-muted)" }}>No upcoming appointments scheduled.</p>
                            )}
                        </div>
                        <div className="glass-panel" style={{ padding: "30px" }}>
                            <h3>Overview</h3>
                            {overviewData ? (
                                <pre style={{ marginTop: "10px", color: "var(--text-muted)", fontSize: "0.9em" }}>
                                    {JSON.stringify(overviewData, null, 2)}
                                </pre>
                            ) : (
                                <p style={{ marginTop: "10px", color: "var(--text-muted)" }}>Your overview is looking good.</p>
                            )}
                        </div>
                        <div className="glass-panel" style={{ padding: "30px" }}>
                            <h3>Recent Notifications</h3>
                            <p style={{ marginTop: "10px", color: "var(--text-muted)" }}>You have {unreadCount} unread messages.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}