import React, { createContext, useContext, useEffect, useState } from "react";
import { userData } from "../api/auth";

interface User {
  username: string;
  email: string;
  profile_image?: string | null;
  role: string; 
  id: number; 
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  token: string | null;
  loginWithToken: (token: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [loading, setLoading] = useState<boolean>(true);

  const fetchUser = async (authToken: string) => {
    setLoading(true);
    try {
      const res = await userData({
        headers: { Authorization: `Bearer ${authToken}` },
      });
      console.log("Pobrano dane użytkownika:", res.data);
  
      const mappedUser: User = {
        username: res.data.username,
        email: res.data.email,
        role: String(res.data.user_role),
        profile_image: res.data.profile_image || null,
        id: res.data.id, 
      };
  
      setUser(mappedUser);
    } catch (err) {
      console.error("Błąd przy pobieraniu użytkownika:", err);
      setToken(null);
      localStorage.removeItem("token");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchUser(token);
    } else {
      setLoading(false);
    }
  }, [token]);

  const loginWithToken = async (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    await fetchUser(newToken); 
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, token, loginWithToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
};
