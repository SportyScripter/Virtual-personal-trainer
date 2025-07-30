import React, { useState, useEffect } from 'react';
import MainLayout from '../components/MainLayout';
import { getMyExercises, deleteExercise, UserExercise } from '../services/api';
import { Trash2, Video } from 'lucide-react'; 

const VideoModal = ({ exercise, onClose }: { exercise: UserExercise; onClose: () => void }) => {
    const videoUrl = `http://localhost:8080/videos/${exercise.videos[0]?.video_path}`;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" onClick={onClose}>
          <div className="bg-gray-800 p-6 rounded-lg max-w-3xl w-full" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-2xl font-bold text-white mb-4">{exercise.exercise_name}</h2>
            {exercise.videos.length > 0 ? (
              <video src={videoUrl} controls autoPlay className="w-full rounded-md mb-4">
                Twoja przeglądarka nie obsługuje tagu wideo.
              </video>
            ) : (
              <p className="text-gray-400 mb-4">Brak wideo dla tego ćwiczenia.</p>
            )}
            <h3 className="text-lg font-semibold text-white">Opis:</h3>
            <p className="text-gray-300 mt-2">{exercise.description || 'Brak opisu.'}</p>
            <button onClick={onClose} className="mt-6 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
              Zamknij
            </button>
          </div>
        </div>
      );
    };

    const MyExercisesPage = () => {
        const [exercises, setExercises] = useState<UserExercise[]>([]);
        const [isLoading, setIsLoading] = useState(true);
        const [error, setError] = useState<string | null>(null);
        const [selectedExercise, setSelectedExercise] = useState<UserExercise | null>(null);
      
        useEffect(() => {
          const fetchExercises = async () => {
            try {
              const data = await getMyExercises();
              setExercises(data);
            } catch (err: any) {
              setError(err.message);
            } finally {
              setIsLoading(false);
            }
          };
          fetchExercises();
        }, []);
      
        const handleDelete = async (exerciseId: number) => {
          if (window.confirm("Czy na pewno chcesz usunąć to ćwiczenie i wszystkie powiązane z nim wideo?")) {
              try {
                  await deleteExercise(exerciseId);
                  setExercises(prev => prev.filter(ex => ex.id !== exerciseId));
              } catch (err: any) {
                  setError(err.message);
              }
          }
        };
      
        const renderContent = () => {
          if (isLoading) return <p className="text-white">Ładowanie Twoich ćwiczeń...</p>;
          if (error) return <p className="text-red-500">Błąd: {error}</p>;
          if (exercises.length === 0) return <p className="text-white">Nie dodałeś jeszcze żadnych ćwiczeń.</p>;
      
          return (
            <div className="bg-gray-800 shadow-md rounded-lg p-4">
              <ul className="divide-y divide-gray-700">
                {exercises.map((exercise) => (
                  <li key={exercise.id} className="py-4 flex items-center justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <p 
                        className="text-sm font-medium text-indigo-400 truncate cursor-pointer hover:underline"
                        onClick={() => setSelectedExercise(exercise)}
                      >
                        {exercise.exercise_name}
                      </p>
                      <p className="text-sm text-gray-400">{exercise.body_part_name}</p>
                    </div>
                    <div className="text-sm text-gray-500 hidden md:block">
                      {exercise.videos.length > 0 ? new Date(exercise.videos[0].create_at).toLocaleDateString() : 'Brak wideo'}
                    </div>
                    <div className="text-sm text-gray-500 truncate hidden lg:block" title={exercise.videos[0]?.video_path}>
                      {exercise.videos.length > 0 ? <Video className="inline-block" size={16}/> : 'Brak'}
                    </div>
                    <button onClick={() => handleDelete(exercise.id)} className="text-red-500 hover:text-red-400 flex-shrink-0">
                      <Trash2 size={20} />
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          );
        };
      
        return (
          <MainLayout>
            <h1 className="text-3xl font-bold mb-6 text-white">Moje Ćwiczenia</h1>
            {renderContent()}
            {selectedExercise && <VideoModal exercise={selectedExercise} onClose={() => setSelectedExercise(null)} />}
          </MainLayout>
        );
      };
      
      export default MyExercisesPage;
      
