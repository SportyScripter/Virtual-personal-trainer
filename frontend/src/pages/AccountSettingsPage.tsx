import React from 'react';
import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useAuth } from '../context/AuthContext';
import { uploadProfileImage } from '../services/api';
import MainLayout from '../components/MainLayout';
import { Camera } from 'lucide-react';

const AccountSettingsPage = () => {
  const { user, updateUserContext } = useAuth(); 
  const [newImageFile, setNewImageFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles?.length) {
      const file = acceptedFiles[0];
      setNewImageFile(file);
      const previewUrl = URL.createObjectURL(file);
      setPreview(previewUrl);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/jpeg': [], 'image/png': [] },
    maxFiles: 1,
    multiple: false,
  });

  const handleUpload = async () => {
    if (!newImageFile) return;

    setIsLoading(true);
    setError(null);

    try {
      const updatedUser = await uploadProfileImage(newImageFile);
      updateUserContext(updatedUser); 
      alert('Zdjęcie profilowe zostało zaktualizowane!');
      setNewImageFile(null);
      setPreview(null);
      window.location.reload();
    } catch (err: any) {
      setError(err.message || 'Wystąpił nieoczekiwany błąd.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const currentImageUrl = user?.profile_image 
    ? `http://localhost:8080${user.profile_image}` 
    : '/images/avatar.png';

  return (
    <MainLayout>
      <h1 className="text-3xl font-bold mb-6 text-white">Ustawienia Konta</h1>
      <div className="bg-gray-800 p-8 rounded-lg max-w-md mx-auto">
        <div className="flex flex-col items-center">
          <div {...getRootProps()} className="relative cursor-pointer group">
            <img
              src={preview || currentImageUrl}
              alt="Zdjęcie profilowe"
              className="w-40 h-40 rounded-full object-cover border-4 border-gray-600 group-hover:opacity-50 transition-opacity"
            />
            <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
              <Camera className="text-white" size={48} />
            </div>
            <input {...getInputProps()} />
          </div>
          
          {isDragActive && <p className="mt-4 text-indigo-400">Upuść zdjęcie tutaj...</p>}

          <div className="mt-6 w-full">
            {newImageFile && (
              <div className="flex flex-col items-center">
                <p className="text-gray-300 mb-4">Wybrano: {newImageFile.name}</p>
                <button
                  onClick={handleUpload}
                  disabled={isLoading}
                  className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:bg-gray-500"
                >
                  {isLoading ? 'Zapisywanie...' : 'Zapisz nowe zdjęcie'}
                </button>
              </div>
            )}
          </div>
          {error && <p className="mt-4 text-red-500">{error}</p>}
        </div>
      </div>
    </MainLayout>
  );
};

export default AccountSettingsPage;
