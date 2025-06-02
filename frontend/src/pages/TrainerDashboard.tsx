import { useEffect, useState } from "react";
import { userData } from "../api/auth";
import { ConstSizeButton } from "../components/Button";
interface User {
  username: string;
  email: string;
  profile_image?: string; 
}


const TrainerDashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const res = await userData({
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(res.data);
      } catch (err) {
        console.error("Błąd podczas pobierania danych użytkownika", err);
      }
    };

    fetchUser();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  if (!user) return <div>Ładowanie...</div>;

  return (
    <div className="flex min-h-screen">
      {/* Dashboard po lewej stronie */}
      <aside className="w-64 border-r border-gray-300 p-6 bg-gray-300">
        <div className="flex flex-col items-center">
          <div className="mb-6 text-center">
            <p className="text-sm font-medium">{currentTime.toLocaleDateString()}</p>
            <p className="text-lg font-semibold">{currentTime.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}</p>
          </div>
          <img
            src={user.profile_image || "/images/avatar.png"} 
            alt="avatar"
            className="w-20 h-20 rounded-full mb-4"
          />
          <h3 className="text-xl font-semibold mb-1">{user.username}</h3>
          <p className="text-sm mb-12 text-gray-600">{user.email}</p>
          <ConstSizeButton>Dodaj ćwiczenie</ConstSizeButton>
          <ConstSizeButton>Moi podopieczni</ConstSizeButton>
          <ConstSizeButton>Moje ćwiczenia</ConstSizeButton>
          <ConstSizeButton>Ustawienia Konta</ConstSizeButton>
          <ConstSizeButton>Wyloguj</ConstSizeButton>
        </div>
      </aside>

      {/* Główna zawartość strony */}

      <main className="flex-1 p-8 min-h-screen bg-[url('../public/images/background.png')] bg-cover bg-center bg-white/50">

        {/* Tutaj możesz dodać zawartość strony głównej */}
        <h1 className="text-3xl font-bold mb-4 text-white">Witaj, {user.username}!</h1>
        <p className="text-white">To jest Twoja strona startowa.</p>
      </main>
    </div>
  );
}
export default TrainerDashboard;