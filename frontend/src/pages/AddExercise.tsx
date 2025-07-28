import React, { useState, useEffect } from 'react';
import MainLayout from '../components/MainLayout'; 
import { getBodyParts } from '../services/api';

interface BodyPart {
  id: number;
  body_part_name: string;
}

const AddExercise = () => {
  const [bodyParts, setBodyParts] = useState<BodyPart[]>([]);
  
  const [selectedBodyPart, setSelectedBodyPart] = useState<string>('');
  const [exerciseName, setExerciseName] = useState<string>('');
  const [description, setDescription] = useState<string>('');

  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAndSetBodyParts = async () => {
      try {
        setIsLoading(true);
        const data = await getBodyParts();
        setBodyParts(data);
        setError(null);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAndSetBodyParts();
  }, []); 

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedBodyPart) {
        alert("Proszę wybrać partię mięśniową!");
        return;
    }
    // TODO: Zaimplementować endpoint POST w backendzie
    console.log("Dane do wysłania:", {
      bodyPartId: parseInt(selectedBodyPart, 10),
      name: exerciseName,
      description: description,
    });
    alert("Ćwiczenie zostało (symulacyjnie) zapisane! Sprawdź konsolę.");
  };

  const renderContent = () => {
    if (isLoading) {
      return <p className="text-white">Ładowanie partii mięśniowych...</p>;
    }
    if (error) {
      return <p className="text-red-500">Błąd: {error}</p>;
    }
    return (
      <form onSubmit={handleSubmit} className="space-y-4 max-w-lg">
        <div>
          <label htmlFor="body-part" className="block text-sm font-medium text-gray-300 mb-1">
            Partia mięśniowa
          </label>
          <select
            id="body-part"
            value={selectedBodyPart}
            onChange={(e) => setSelectedBodyPart(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
            required
          >
            <option value="" disabled>Wybierz partię...</option>
            {bodyParts.map((part) => (
              <option key={part.id} value={part.id}>
                {part.body_part_name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="exercise-name" className="block text-sm font-medium text-gray-300 mb-1">
            Nazwa ćwiczenia
          </label>
          <input
            type="text"
            id="exercise-name"
            value={exerciseName}
            onChange={(e) => setExerciseName(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
            required
          />
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-300 mb-1">
            Opis (opcjonalnie)
          </label>
          <textarea
            id="description"
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 text-white"
          />
        </div>
        <div>
          <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
            Zapisz ćwiczenie
          </button>
        </div>
      </form>
    );
  };
  
  return (
    <MainLayout>
      <h1 className="text-3xl font-bold mb-6 text-white">Dodaj nowe ćwiczenie</h1>
      {renderContent()}
    </MainLayout>
  );
};

export default AddExercise;