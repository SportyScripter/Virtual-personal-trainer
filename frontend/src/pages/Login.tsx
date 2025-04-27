import React, { useState } from "react";
import Input from "../components/Input";
import Button from "../components/Button";
import { login } from "../api/auth";
import { useNavigate } from "react-router-dom"; 
const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await login(formData);
      console.log(res.data);
      localStorage.setItem("token", res.data.access_token);
      alert("Logged in successfully!");
    } catch (error: any) {
      console.error(error.response.data.detail);
      alert(error.response.data.detail);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Login</h1>
      <form onSubmit={handleSubmit} className="w-80">
        <Input label="Email" name="email" value={formData.email} onChange={handleChange} />
        <Input label="Password" name= "password" type="password" value={formData.password} onChange={handleChange} />
        <Button type="submit">Login</Button>
      </form>
    </div>
  );
};

export default Login;
