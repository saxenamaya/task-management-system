import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import { useAuth } from "./context/AuthContext";

import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import CreateTaskPage from "./pages/CreateTaskPage";
import CreateRulePage from "./pages/CreateRulePage";
import EligibleUsersPage from "./pages/EligibleUsersPage";
import EligibleTasksPage from "./pages/EligibleTasksPage";

import DashboardLayout from "./layouts/DashboardLayout";

export default function App() {
  const { token } = useAuth();

  if (!token) {
    return <LoginPage />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/tasks/create" element={<CreateTaskPage />} />
          <Route path="/rules/create" element={<CreateRulePage />} />
          <Route path="/eligible-users" element={<EligibleUsersPage />} />
          <Route path="/eligible-tasks" element={<EligibleTasksPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}