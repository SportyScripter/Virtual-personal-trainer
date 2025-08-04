import React from "react";
import Header from "./Header";
import { UserSidebar, TrainerSidebar } from "./Sidebar";
import { useAuth } from "../context/AuthContext";

interface Props {
  children: React.ReactNode;
}

const MainLayout: React.FC<Props> = ({ children }) => {
  const { user, loading } = useAuth(); 

  const renderSidebar = () => {
    if (loading) {
      return <aside className="w-64 border-r border-gray-300 p-6 bg-gray-300"></aside>;
    }

    if (user?.role === "1") {
      return <UserSidebar />;
    }

    if (user?.role === "2") {
      return <TrainerSidebar />;
    }

    return null; 
  };

  return (
    <div>
      <Header />
      <div className="flex min-h-screen">
        {renderSidebar()}
        
        <main className="flex-1 p-8 min-h-screen bg-[url('../public/images/background.png')] bg-cover bg-center bg-white/50">
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;