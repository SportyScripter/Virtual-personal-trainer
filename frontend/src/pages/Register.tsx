import React, { useState } from "react";
import Input from "../components/Input";
import {Button} from "../components/Button";
import { register } from "../api/auth"; 
import { useNavigate } from "react-router-dom"; 

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    first_name: "",
    last_name: "",
    user_role: "",
  });

  const [errors, setErrors] = useState<{ [key: string]: string }>({});


  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  
  

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: { [key: string]: string } = {};
  
    if (!formData.email) newErrors.email = "Email jest wymagany";
    if (!formData.password) newErrors.password = "Hasło jest wymagane";
    if (!formData.username) newErrors.username = "Nazwa użytkownika jest wymagana";
    if (!formData.first_name) newErrors.first_name = "Imię jest wymagane";
    if (!formData.last_name) newErrors.last_name = "Nazwisko jest wymagane";
    if (!formData.user_role) newErrors.user_role = "Rola jest wymagana";
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    try {
        await register(formData);
        alert('Rejestracja zakończona sukcesem!');
        navigate('/login')
      } catch (error) {
        alert('Błąd podczas rejestracji'+ error);
        console.log(JSON.stringify(formData, null, 2));
      }
  };



  return (
    <div className="min-h-screen bg-[url('../public/images/background.png')] bg-cover bg-center">

    <div className="shadow-lg p-8 flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-5xl font-bold mb-6 text-center text-white">Register</h1>
      <form onSubmit={handleSubmit} className="w-80 space-y-4 text-black">
        <Input label="Email" name="email" value={formData.email} onChange={handleChange} error={errors.email} />
        <Input label="Username" name="username" value={formData.username} onChange={handleChange} error={errors.username}/>
        <Input label="Password" name= "password" type="password" value={formData.password} onChange={handleChange} error={errors.password}/>
        <Input label="First Name" name="first_name" value={formData.first_name} onChange={handleChange} error={errors.first_name}/>
        <Input label="Last Name" name="last_name" value={formData.last_name} onChange={handleChange} error={errors.last_name}/>
        <div className="flex flex-col">
          <label className="mb-1 font-semibold text-white">Role:</label>
          <select name="user_role" value={formData.user_role} onChange={handleChange} className="border border-gray-300 rounded-md p-2">
            <option value="">Select a role</option>
            <option value="1">User</option>
            <option value="2">Trainer</option>
          </select>
          {errors.user_role && <p className="text-red-500 text-sm">{errors.user_role}</p>}
        </div>
  
        <Button type="submit">Register</Button>
        <Button type="button" onClick={() => navigate("/login")}>Anuluj</Button>
      </form>
    </div>
    </div>
  );
}


export default Register;
