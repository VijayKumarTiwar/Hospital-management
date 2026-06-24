import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Register from "./pages/Register";

export default function AppRoutes() {

    return (

        <Routes>

            <Route path="/" element={<Login />} />

            <Route path="/register" element={<Register />} />

            <Route path="/dashboard" element={<Dashboard />} />

        </Routes>

    );

}