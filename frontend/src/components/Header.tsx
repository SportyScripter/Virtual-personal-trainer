import React from "react";
import { Link } from "react-router-dom"; 

const Header: React.FC = () => {
  return (
    <header className="w-full text-center bg-gray-500 bg-cover bg-center p-4 text-white">
      <h1 className="text-2xl font-bold mb-2">Virtual Personal Trainer</h1>
      <nav>
        <ul className="flex justify-center space-x-6">
          <li>
            <Link to="/">Strona główna</Link>
          </li>
          <li>
            <Link to="/about">O nas</Link>
          </li>
          <li>
            <Link to="/contact">Kontakt</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
