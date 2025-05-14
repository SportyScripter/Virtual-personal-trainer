import React from "react";

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit";
}

export const Button: React.FC<ButtonProps> = ({ children, onClick, type = "button" }) => (
  <button
    onClick={onClick}
    type={type}
    className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition mb-2"
  >
    {children}
  </button>
);

export const PrimaryButton: React.FC<ButtonProps> = ({ children, onClick, type = "button" }) => (
  <button
    onClick={onClick}
    type={type}
    className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition mb-2"
  >
    {children}
  </button>
);

// Przyciski dodatkowe (np. szary, czerwony)
export const SecondaryButton: React.FC<ButtonProps> = ({ children, onClick, type = "button" }) => (
  <button
    onClick={onClick}
    type={type}
    className="bg-green-500 text-black p-2 rounded-lg hover:bg-green-700 transition mb-2"
  >
    {children}
  </button>
);


export const DangerButton: React.FC<ButtonProps> = ({ children, onClick, type = "button" }) => (
  <button
    onClick={onClick}
    type={type}
    className="bg-red-500 text-white p-2 rounded-lg hover:bg-red-600 transition mb-2"
  >
    {children}
  </button>
);

export const ConstSizeButton: React.FC<ButtonProps> = ({ children, onClick, type = "button" }) => (
  <button
    onClick={onClick}
    type={type}
    className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition mb-4"
    style={{ width: "150px", height: "50px", marginRight: "10px" }} // Ustalona szerokość i wysokość
  >
    {children}
  </button>
);

export const SmallButton: React.FC<ButtonProps> = ({ children, onClick, type = "button" }) => (
  <button
    onClick={onClick}
    type={type}
    className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition mb-2"
  >
    {children}
  </button>
);


