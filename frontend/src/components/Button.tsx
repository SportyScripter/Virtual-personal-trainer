import React from "react";

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit";
}

const Button: React.FC<ButtonProps> = ({ children, onClick, type = "button" }) => (
  <button
    onClick={onClick}
    type={type}
    className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition"
  >
    {children}
  </button>
);

export default Button;
