import MainLayout from "../components/MainLayout";

const TrainerDashboard = () => {

  if (!localStorage.getItem("username") == null) return <div>Ładowanie...</div>;

  return (
<MainLayout>
        <h1 className="text-3xl font-bold mb-4 text-white">Witaj, {localStorage.getItem("username")}!</h1>
        <p className="text-white">To jest Twoja strona startowa.</p>
    </MainLayout>
  );
};
export default TrainerDashboard;