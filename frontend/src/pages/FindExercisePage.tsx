import React, { useState, useEffect } from 'react';
import MainLayout from '../components/MainLayout';
import { getBodyParts, getExercisesByBodyPart, ExerciseWithTrainer } from '../services/api'; 

interface BodyPart {
  id: number;
  body_part_name: string;
}

const FindExercisePage = () => {
  const [bodyParts, setBodyParts] = useState<BodyPart[]>([]);
  const [selectedBodyPart, setSelectedBodyPart] = useState<BodyPart | null>(null);
  const [exercises, setExercises] = useState<ExerciseWithTrainer[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

  const handleSelectBodyPart = async (part: BodyPart) => {
    setSelectedBodyPart(part);
    setIsLoading(true);
    setError(null);
    try {
      const exercisesData = await getExercisesByBodyPart(part.id);
      setExercises(exercisesData);
    } catch (err: any) {
      setError(err.message);
      setExercises([]);
    } finally {
      setIsLoading(false);
    }
  };

  const renderExercisesTable = () => (
    <div>
      <button 
        onClick={() => setSelectedBodyPart(null)} 
        className="mb-6 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-500 transition-colors"
      >
        &larr; Wróć do wyboru partii
      </button>
      <h2 className="text-2xl font-semibold text-white mb-4">
        Ćwiczenia dla: <span className="text-indigo-400">{selectedBodyPart?.body_part_name}</span>
      </h2>
      {isLoading ? (
        <p className="text-white">Ładowanie ćwiczeń...</p>
      ) : exercises.length > 0 ? (
        <div className="overflow-x-auto bg-gray-800 rounded-lg">
          <table className="min-w-full text-sm text-left text-gray-300">
            <thead className="text-xs text-gray-400 uppercase bg-gray-700">
              <tr>
                <th scope="col" className="px-6 py-3">Nazwa ćwiczenia</th>
                <th scope="col" className="px-6 py-3">Dodane przez</th>
              </tr>
            </thead>
            <tbody>
              {exercises.map(exercise => (
                <tr key={exercise.id} className="border-b border-gray-700 hover:bg-gray-600">
                  <td className="px-6 py-4 font-medium text-white">{exercise.exercise_name}</td>
                  <td className="px-6 py-4">{`${exercise.user.first_name} ${exercise.user.last_name}`}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-white">Brak dostępnych ćwiczeń dla tej partii ciała.</p>
      )}
    </div>
  );

  const renderBodyPartSelection = () => (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
       {bodyParts.map((part) => (
         <button
           key={part.id}
           onClick={() => handleSelectBodyPart(part)}
           className="p-6 bg-gray-700 rounded-lg text-white font-semibold text-center hover:bg-indigo-600 transition-colors"
         >
           {part.body_part_name}
         </button>
       ))}
     </div>
 );
  return (
    <MainLayout>
      <h1 className="text-3xl font-bold mb-6 text-white">Znajdź Ćwiczenie</h1>
      {isLoading && !selectedBodyPart && <p className="text-white">Ładowanie partii ciała...</p>}
      {error && <p className="text-red-500">Błąd: {error}</p>}
      
      {!isLoading && (selectedBodyPart ? renderExercisesTable() : renderBodyPartSelection())}
    </MainLayout>
  );
};

export default FindExercisePage;

