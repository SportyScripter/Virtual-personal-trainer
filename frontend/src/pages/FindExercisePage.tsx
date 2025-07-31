// src/pages/FindExercisePage.tsx

import React, { useState, useEffect } from 'react';
import MainLayout from '../components/MainLayout';
import { getBodyParts } from '../services/api'; 

// Definicja typu dla partii ciała
interface BodyPart {
  id: number;
  body_part_name: string;
}

const FindExercisePage = () => {
  const [bodyParts, setBodyParts] = useState<BodyPart[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pobieranie listy partii ciała przy pierwszym załadowaniu strony
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const parts = await getBodyParts();
        setBodyParts(parts);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchInitialData();
  }, []);

  // Funkcja renderująca zawartość strony
  const renderContent = () => {
    if (isLoading) {
      return <p className="text-white">Ładowanie partii ciała...</p>;
    }
    if (error) {
      return <p className="text-red-500">Błąd: {error}</p>;
    }

    // Widok wyboru partii ciała w formie siatki
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {bodyParts.map((part) => (
          <button
            key={part.id}
            // Na razie kliknięcie nic nie robi, dodamy to w następnym kroku
            onClick={() => alert(`Wybrano: ${part.body_part_name}`)}
            className="p-6 bg-gray-700 rounded-lg text-white font-semibold text-center hover:bg-indigo-600 transition-colors"
          >
            {part.body_part_name}
          </button>
        ))}
      </div>
    );
  };

  return (
    <MainLayout>
      <h1 className="text-3xl font-bold mb-6 text-white">Znajdź Ćwiczenie</h1>
      {renderContent()}
    </MainLayout>
  );
};

export default FindExercisePage;
