import React, { useState, useEffect, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import MainLayout from '../components/MainLayout';
import { getBodyParts, createExercise, uploadExerciseVideo } from '../services/api';
import { useAuth } from "../context/AuthContext";

interface BodyPart {
  id: number;
  body_part_name: string;
}

const AddExercise = () => {
  const { user } = useAuth();
  
  const [bodyParts, setBodyParts] = useState<BodyPart[]>([]);
  const [selectedBodyPart, setSelectedBodyPart] = useState<string>('');
  const [exerciseName, setExerciseName] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [videoFile, setVideoFile] = useState<File | null>(null);
  
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isDataLoading, setIsDataLoading] = useState<boolean>(true); 
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAndSetBodyParts = async () => {
      try {
        const data = await getBodyParts();
        setBodyParts(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsDataLoading(false);
      }
    };
    fetchAndSetBodyParts();
  }, []); 
  
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles?.length) {
      setVideoFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'video/*': ['.mp4', '.mov'] },
    maxFiles: 1,
    multiple: false,
  });

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!selectedBodyPart || !exerciseName || !user) {
      setError("Proszę wypełnić wszystkie wymagane pola.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const exerciseData = {
        exercise_name: exerciseName,
        body_part_id: parseInt(selectedBodyPart, 10),
        description: description,
        user_id: user.id,
      };
      
      const newExercise = await createExercise(exerciseData);

      if (videoFile && newExercise.id) {
        const videoUploadData = {
            exerciseId: newExercise.id,
            userId: user.id,
            bodyPartId: parseInt(selectedBodyPart, 10),
            videoFile: videoFile,
        };
        
        await uploadExerciseVideo(videoUploadData);
      }

      alert("Ćwiczenie zostało pomyślnie dodane!");
      
      setExerciseName('');
      setDescription('');
      setSelectedBodyPart('');
      setVideoFile(null);

    } catch (err: any) {
      setError(err.message || "Wystąpił nieoczekiwany błąd podczas zapisywania.");
    } finally {
      setIsLoading(false);
    }
  };

  const renderContent = () => {
    if (isDataLoading) {
      return <p className="text-white">Ładowanie danych...</p>;
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
        <div {...getRootProps()} className={`p-8 border-2 border-dashed rounded-md text-center cursor-pointer transition-colors ${isDragActive ? 'border-indigo-500 bg-gray-800' : 'border-gray-600'} ${videoFile ? 'border-green-500' : ''}`}>
          <input {...getInputProps()} />
          {videoFile ? (<div className="text-green-400"><p>Plik gotowy: {videoFile.name}</p></div>) : isDragActive ? (<p className="text-indigo-400">Upuść plik tutaj...</p>) : (<p className="text-gray-400">Przeciągnij plik wideo lub kliknij</p>)}
        </div>
        {videoFile && (<button type="button" onClick={() => setVideoFile(null)} className="mt-2 text-sm text-red-500 hover:text-red-400">Usuń plik</button>)}
        {error && <p className="text-red-500 mt-2">{error}</p>}
        <div>
          <button type="submit" disabled={isLoading} className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:bg-gray-500">
            {isLoading ? 'Zapisywanie...' : 'Zapisz ćwiczenie'}
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