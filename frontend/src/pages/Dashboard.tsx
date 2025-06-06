import { useAuth } from "../context/AuthContext";
import UserDashboard from "./UserDashboard";
import TrainerDashboard from "./TrainerDashboard";

const Dashboard = () => {
  const { user } = useAuth();

  if (!user) return <div>Ładowanie...</div>;

  return user.role === "1" ? <TrainerDashboard /> : <UserDashboard />;
};

export default Dashboard;
