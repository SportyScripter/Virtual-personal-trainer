import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import UserDashboard from "./pages/UserDashboard"; 
import TrainerDashboard from "./pages/TrainerDashboard"; 
import StartPage from "./pages/StarPage"
import Dashboard from "./pages/Dashboard";
import { ProtectedRoute } from "./components/ProtectRoute";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/UserDashboard" element={<UserDashboard />} />
        <Route path="/TrainerDashboard" element={<TrainerDashboard />} />
        <Route path="/dashboard"element={<ProtectedRoute><Dashboard /></ProtectedRoute>}/>
      </Routes>
    </Router>
  );
}

export default App;
