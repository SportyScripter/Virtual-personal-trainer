import React from "react";
import {ConstSizeButton} from "../components/Button";
import { useNavigate } from "react-router-dom"; 

const StartPage = () => {
    const navigate = useNavigate(); 
  
    const handleLoginClick = () => {
      navigate("/login");
    };
  
    const handleRegisterClick = () => {
      navigate("/register");
    };



    return(
        <div className="min-h-screen bg-[url('../public/images/background.png')] bg-cover bg-center">
        <div className="flex flex-col items-center justify-center min-h-screen">
            <img src="../public/images/logo2.png" className="size-96 rounded-full" ></img>
            <h1 className="text-6xl font-bold mb-6 text-center text-cyan-500 font-serif">WELCOME</h1>
            <h1 className="text-2xl font-bold mb-6 text-center text-cyan-500 font-serif">Check your technique!</h1>
            <div className="flex gap-4">
            <ConstSizeButton onClick={handleRegisterClick}>Register</ConstSizeButton>
            <ConstSizeButton onClick={handleLoginClick}>Login</ConstSizeButton>
            </div>
        </div>  
        </div>
)
}

export default StartPage;  