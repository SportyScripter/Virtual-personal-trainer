import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token, loading } = useAuth();

  if (loading) return <div>Ładowanie...</div>;

  if (!token) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
};
