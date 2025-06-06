import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "./Header";
import { UserSidebar, TrainerSidebar } from "./Sidebar";

interface Props {
  children: React.ReactNode;
}

const MainLayout: React.FC<Props> = ({ children }) => {
  const [role, setRole] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedRole = localStorage.getItem("user_role");
    if (!storedRole) {
      navigate("/login");
    } else {
      setRole(storedRole);
    }
  }, []);

  const username = localStorage.getItem("username");
  const email = localStorage.getItem("email");
  const profileImage = localStorage.getItem("profile_image") ?? undefined;

  return (
    <div>
      <Header />
      <div className="flex min-h-screen">
        {role === "1" && (
          <UserSidebar username={username} email={email} profileImage={"/images/avatar.png"} />
        )}
        {role === "2" && (
          <TrainerSidebar username={username} email={email} profileImage={"/images/avatar2.png"} />
        )}
        <main className="flex-1 p-8 min-h-screen bg-[url('../public/images/background.png')] bg-cover bg-center bg-white/50">

          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
