
import axios from 'axios';

interface BodyPart {
  id: number;
  body_part_name: string;
}

const apiClient = axios.create({
  baseURL: 'http://localhost:8080', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getBodyParts = async (): Promise<BodyPart[]> => {
  try {
    const response = await apiClient.get<BodyPart[]>('/body_parts/list');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Wystąpił błąd podczas pobierania danych");
    }
    throw new Error("Nie można połączyć się z serwerem");
  }
};

interface ExerciseCreateData {
  exercise_name: string;
  body_part_id: number;
  description: string;
  user_id: number;
}

interface ExerciseResponse {
  id: number;
  exercise_name: string;
  body_part_id: number;
  description: string | null;
  user_id: number;
}

interface UploadVideoData {
  exerciseId: number;
  userId: number;
  bodyPartId: number;
  videoFile: File;
}

export const createExercise = async (data: ExerciseCreateData): Promise<ExerciseResponse> => {
  try {
    const response = await apiClient.post<ExerciseResponse>('/exercise/create_exercise', data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Błąd podczas tworzenia ćwiczenia");
    }
    throw new Error("Nie można utworzyć ćwiczenia. Sprawdź połączenie z serwerem.");
  }
};

export const uploadExerciseVideo = async (data: UploadVideoData): Promise<void> => {
  const formData = new FormData();

  // Dodajemy wszystkie dane wymagane przez endpoint backendu jako pola formularza
  formData.append('file', data.videoFile);
  formData.append('user_id', data.userId.toString());
  formData.append('body_part_id', data.bodyPartId.toString());

  try {
    // ID ćwiczenia jest częścią URL, reszta danych jest w ciele formularza
    // Używamy poprawionej ścieżki z backendu
    await apiClient.post(`/exercise_video/upload_video/${data.exerciseId}`, formData, {
      headers: {
        // Przeglądarka sama ustawi poprawny Content-Type z 'boundary' dla FormData
        'Content-Type': 'multipart/form-data',
      },
    });
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Błąd podczas wysyłania pliku wideo");
    }
    throw new Error("Nie można było wysłać pliku wideo. Sprawdź połączenie z serwerem.");
  }
};