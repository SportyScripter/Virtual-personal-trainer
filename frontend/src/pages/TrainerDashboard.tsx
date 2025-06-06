import MainLayout from "../components/MainLayout";
import { useAuth } from "../context/AuthContext";

const TrainerDashboard = () => {
  const { user } = useAuth();

  if (!localStorage.getItem("username") == null) return <div>Ładowanie...</div>;

  return (
<MainLayout>
        <h1 className="text-3xl font-bold mb-4 text-white">Witaj, {user?.username}!</h1>
        <p className="text-white">To jest Twoja strona startowa.</p>
    </MainLayout>
  );
};
export default TrainerDashboard;