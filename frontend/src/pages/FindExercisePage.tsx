import React, { useState, useEffect, useCallback } from 'react';
import MainLayout from '../components/MainLayout';
import { getBodyParts, getExercisesByBodyPart, ExerciseWithTrainer, ExerciseDetails, getExerciseDetails, compareTechnique, AnalysisResult } from '../services/api';
import { ArrowLeft, UploadCloud } from 'lucide-react';
import { useDropzone } from 'react-dropzone';

interface BodyPart {
    id: number;
    body_part_name: string;
}

const FindExercisePage = () => {
    const [bodyParts, setBodyParts] = useState<BodyPart[]>([]);
    const [selectedBodyPart, setSelectedBodyPart] = useState<BodyPart | null>(null);
    const [exercises, setExercises] = useState<ExerciseWithTrainer[]>([]);
    const [selectedExerciseDetails, setSelectedExerciseDetails] = useState<ExerciseDetails | null>(null);
    const [isModalLoading, setIsModalLoading] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [trainerVideoToCompare, setTrainerVideoToCompare] = useState<string | null>(null);

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

    const handleExerciseClick = async (exerciseId: number) => {
        setIsModalLoading(true);
        setError(null);
        try {
            const details = await getExerciseDetails(exerciseId);
            setSelectedExerciseDetails(details);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsModalLoading(false);
        }
    };

    const handleCompareTechnique = (videoPath: string) => {
        console.log("Wybrano wideo do porównania:", videoPath);
        alert("Ścieżka do wideo została zapisana! (Sprawdź konsolę)");
        setSelectedExerciseDetails(null);
        setTrainerVideoToCompare(videoPath);
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
                                <tr
                                    key={exercise.id}
                                    className="border-b border-gray-700 hover:bg-gray-600 cursor-pointer"
                                    onClick={() => handleExerciseClick(exercise.id)}
                                >
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
                    key={part.id} onClick={() => handleSelectBodyPart(part)} className="p-6 bg-gray-700 rounded-lg text-white font-semibold text-center hover:bg-indigo-600 transition-colors">
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
            {(isModalLoading || selectedExerciseDetails) && (
                isModalLoading ? (
                    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
                        <p className="text-white">Ładowanie szczegółów...</p>
                    </div>
                ) : selectedExerciseDetails && (
                    <ExerciseDetailModal
                        exercise={selectedExerciseDetails}
                        onClose={() => setSelectedExerciseDetails(null)}
                        onCompare={handleCompareTechnique}
                    />
                )
            )}
            {trainerVideoToCompare && (
                <CompareTechniqueModal
                    trainerVideoPath={trainerVideoToCompare}
                    onClose={() => setTrainerVideoToCompare(null)}
                />
            )}
        </MainLayout>
    );
};

const ExerciseDetailModal = ({ exercise, onClose, onCompare }: { exercise: ExerciseDetails, onClose: () => void, onCompare: (videoPath: string) => void }) => {
    const videoUrl = exercise.video_path ? `http://localhost:8080/videos/${exercise.video_path}` : '';

    return (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" onClick={onClose}>
            <div className="bg-gray-800 p-6 rounded-lg max-w-3xl w-full mx-4" onClick={(e) => e.stopPropagation()}>
                <h2 className="text-2xl font-bold text-white mb-4">{exercise.exercise_name}</h2>

                {videoUrl ? (
                    <video src={videoUrl} controls autoPlay className="w-full rounded-md mb-4 bg-black">
                        Twoja przeglądarka nie obsługuje tagu wideo.
                    </video>
                ) : (
                    <div className="w-full aspect-video bg-black flex items-center justify-center rounded-md mb-4">
                        <p className="text-gray-500">Brak wideo dla tego ćwiczenia.</p>
                    </div>
                )}

                <h3 className="text-lg font-semibold text-white">Opis:</h3>
                <p className="text-gray-300 mt-2 mb-6">{exercise.description || 'Brak opisu.'}</p>

                <div className="flex justify-between items-center">
                    <button onClick={onClose} className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-500">
                        <ArrowLeft size={18} />
                        Wstecz
                    </button>
                    <button
                        onClick={() => onCompare(videoUrl)}
                        disabled={!videoUrl}
                        className="px-8 py-3 bg-indigo-600 text-white font-bold rounded-md hover:bg-indigo-700 disabled:bg-gray-500 disabled:cursor-not-allowed"
                    >
                        Porównaj technikę
                    </button>
                </div>
            </div>
        </div>
    );
};

const CompareTechniqueModal = ({ trainerVideoPath, onClose }: { trainerVideoPath: string, onClose: () => void }) => {
    const [userVideo, setUserVideo] = useState<File | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles?.length) {
            setUserVideo(acceptedFiles[0]);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'video/*': [] },
        maxFiles: 1,
    });

    const handleAnalyze = async () => {
        if (!userVideo) return;
        setIsLoading(true);
        setError(null);
        try {
            const result = await compareTechnique(userVideo, trainerVideoPath);
            setAnalysisResult(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };
    return (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" onClick={onClose}>
            <div className="bg-gray-800 p-6 rounded-lg max-w-2xl w-full mx-4" onClick={(e) => e.stopPropagation()}>
                {!analysisResult ? (
                    <>
                        <h2 className="text-2xl font-bold text-white mb-4">Porównaj swoją technikę</h2>
                        <div
                            {...getRootProps()}
                            className={`p-10 border-2 border-dashed rounded-md text-center cursor-pointer transition-colors
                    ${isDragActive ? 'border-indigo-500 bg-gray-700' : 'border-gray-600'}
                  `}
                        >
                            <input {...getInputProps()} />
                            <UploadCloud className="mx-auto text-gray-400" size={48} />
                            {userVideo ? (
                                <p className="mt-2 text-green-400">Wybrano plik: {userVideo.name}</p>
                            ) : (
                                <p className="mt-2 text-gray-400">Przeciągnij i upuść swoje wideo lub kliknij, aby wybrać plik</p>
                            )}
                        </div>
                        <button
                            onClick={handleAnalyze}
                            disabled={!userVideo || isLoading}
                            className="w-full mt-6 px-8 py-3 bg-indigo-600 text-white font-bold rounded-md hover:bg-indigo-700 disabled:bg-gray-500"
                        >
                            {isLoading ? 'Analizowanie...' : 'Analizuj'}
                        </button>
                        {error && <p className="mt-4 text-center text-red-500">{error}</p>}
                    </>
                ) : (
                    <>
                        <h2 className="text-2xl font-bold text-white mb-4">Wynik analizy</h2>
                        <img
                            src={`http://localhost:8080${analysisResult.result_image_url}`}
                            alt="Wynik analizy"
                            className="w-full rounded-md bg-black"
                        />
                        <p className="text-center text-gray-300 mt-4">{analysisResult.message}</p>
                        <button onClick={onClose} className="w-full mt-6 px-8 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-500">
                            Zamknij
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};


export default FindExercisePage;

