import React, { useEffect, useState } from "react";
import { ConstSizeButton, LogoutButton } from "./Button";
import TrainerDashboard from "../pages/TrainerDashboard";
import { Link } from "react-router-dom";
interface SidebarProps {
  username: string | null;
  email: string | null;
  profileImage?: string;
}

export const UserSidebar: React.FC<SidebarProps> = ({ username, email, profileImage }) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <aside className="w-64 border-r border-gray-300 p-6 bg-gray-300">
      <div className="flex flex-col items-center">
        <div className="mb-6 text-center">
          <p className="text-sm font-medium">{currentTime.toLocaleDateString()}</p>
          <p className="text-lg font-semibold">
            {currentTime.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
          </p>
        </div>
        <img
          src={profileImage || "/images/avatar.png"}
          alt="avatar"
          className="w-20 h-20 rounded-full mb-4"
        />
        <h3 className="text-xl font-semibold mb-1">{username}</h3>
        <p className="text-sm mb-12 text-gray-600">{email}</p>

        <ConstSizeButton>Ustawienia Konta</ConstSizeButton>
        <ConstSizeButton>Trenerzy</ConstSizeButton>
        <ConstSizeButton>Znajdź ćwiczenie</ConstSizeButton>
        <LogoutButton>Wyloguj</LogoutButton>
      </div>
    </aside>
  );
};


export const TrainerSidebar: React.FC<SidebarProps> = ({ username, email, profileImage }) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <aside className="w-64 border-r border-gray-300 p-6 bg-gray-300">
      <div className="flex flex-col items-center">
        <div className="mb-6 text-center">
          <p className="text-sm font-medium">{currentTime.toLocaleDateString()}</p>
          <p className="text-lg font-semibold">
            {currentTime.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
          </p>
        </div>
        <img
          src={profileImage || "/images/avatar.png"}
          alt="avatar"
          className="w-20 h-20 rounded-full mb-4"
        />
        <h3 className="text-xl font-semibold mb-1">{username}</h3>
        <p className="text-sm mb-12 text-gray-600">{email}</p>

        <ConstSizeButton>Ustawienia Konta</ConstSizeButton>
        <Link to="/addExercise" className="w-full" style={{marginRight: "-40px"}}>
          <ConstSizeButton >Dodaj ćwiczenie</ConstSizeButton>
        </Link>
        <ConstSizeButton>Moi podopieczni</ConstSizeButton>
        <Link to="/my-exercises" className="w-full">
          <ConstSizeButton>Moje ćwiczenia</ConstSizeButton>
        </Link>
        <LogoutButton>Wyloguj</LogoutButton>
      </div>
    </aside>
  );
};
