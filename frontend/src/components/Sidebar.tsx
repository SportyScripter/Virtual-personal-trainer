import React, { useEffect, useState } from "react";
import { ConstSizeButton, LogoutButton } from "./Button";
import { Link } from "react-router-dom";
import { useAuth } from '../context/AuthContext';

interface SidebarProps {}

export const UserSidebar: React.FC<SidebarProps> = () => {
  const { user } = useAuth(); 
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const profileImageUrl = user?.profile_image 
    ? `http://localhost:8080${user.profile_image}` 
    : "/images/avatar.png";

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
          src={profileImageUrl} 
          alt="avatar"
          className="w-20 h-20 rounded-full mb-4 object-cover" 
        />
        <h3 className="text-xl font-semibold mb-1">{user?.username}</h3>
        <p className="text-sm mb-12 text-gray-600">{user?.email}</p>
        
        <Link to="/account-settings" className="w-full" style={{marginRight: "-40px"}}>
          <ConstSizeButton>Ustawienia Konta</ConstSizeButton>
        </Link>
        <ConstSizeButton>Trenerzy</ConstSizeButton>
        <Link to="/find-exercise" className="w-full" style={{marginRight: "-40px"}}>
          <ConstSizeButton>Znajdź ćwiczenie</ConstSizeButton>
        </Link>
        <LogoutButton>Wyloguj</LogoutButton>
      </div>
    </aside>
  );
};


export const TrainerSidebar: React.FC<SidebarProps> = () => {
  const { user } = useAuth(); 
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const profileImageUrl = user?.profile_image 
    ? `http://localhost:8080${user.profile_image}` 
    : "/images/avatar.png";

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
          src={profileImageUrl}
          alt="avatar"
          className="w-20 h-20 rounded-full mb-4 object-cover"
        />
        <h3 className="text-xl font-semibold mb-1">{user?.username}</h3>
        <p className="text-sm mb-12 text-gray-600">{user?.email}</p>

        <Link to="/account-settings" className="w-full" style={{marginRight: "-40px"}}>
          <ConstSizeButton>Ustawienia Konta</ConstSizeButton>
        </Link>
        <Link to="/addExercise" className="w-full" style={{marginRight: "-40px"}}>
          <ConstSizeButton >Dodaj ćwiczenie</ConstSizeButton>
        </Link>
        <ConstSizeButton>Moi podopieczni</ConstSizeButton>
        <Link to="/my-exercises" className="w-full" style={{marginRight: "-40px"}}>
          <ConstSizeButton>Moje ćwiczenia</ConstSizeButton>
        </Link>
        <LogoutButton>Wyloguj</LogoutButton>
      </div>
    </aside>
  );
};
