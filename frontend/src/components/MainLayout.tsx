import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "./Header";
import { UserSidebar, TrainerSidebar } from "./Sidebar";
import { useAuth } from "../context/AuthContext";

interface Props {
  children: React.ReactNode;
}

const MainLayout: React.FC<Props> = ({ children }) => {
  const { user } = useAuth();




  return (
    <div>
      <Header />
      <div className="flex min-h-screen">
        {user?.role === "1" && (
          <UserSidebar username={user?.username ?? null} email={user?.email ?? null} profileImage={"/images/avatar.png"} />
        )}
        {user?.role === "2" && (
          <TrainerSidebar username={user?.username ?? null} email={user?.email ?? null} profileImage={"/images/avatar2.png"} />
        )}
        <main className="flex-1 p-8 min-h-screen bg-[url('../public/images/background.png')] bg-cover bg-center bg-white/50">

          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
