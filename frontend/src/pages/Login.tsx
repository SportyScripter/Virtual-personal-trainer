import React, { useState, useEffect } from "react";
import Input from "../components/Input";
import { Button } from "../components/Button";
import { login, userData } from "../api/auth";
import { useNavigate } from "react-router-dom";

interface User {
  username: string;
  email: string;
  profile_image?: string; 
  user_role?: string;
}

const Login = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [user, setUser] = useState<User | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await login(formData);
      localStorage.setItem("token", res.data.refresh_token);
      alert("Logged in successfully!");

      fetchUserData();
    } catch (error: any) {
      console.error(error.response?.data?.detail || error.message);
      alert(error.response?.data?.detail || "Login failed");
    }
  };

  const fetchUserData = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const res = await userData({
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUser(res.data);

      if (res.data.user_role == "1") {
        navigate("/UserDashboard");
      } else if (res.data.user_role == "2") {
        navigate("/TrainerDashboard");
      } else {
        alert("Invalid role");
      }
    } catch (err) {
      console.error("Błąd podczas pobierania danych użytkownika", err);
    }
  };

  return (
    <div className="min-h-screen bg-[url('../public/images/background.png')] bg-cover bg-center">
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-2xl font-bold mb-6">Login</h1>
        <form onSubmit={handleSubmit} className="w-80">
          <Input label="Email" name="email" value={formData.email} onChange={handleChange} />
          <Input label="Password" name="password" type="password" value={formData.password} onChange={handleChange} />
          <Button type="submit">Login</Button>
        </form>
      </div>
    </div>
  );
};

export default Login;
