
import axios from 'axios';
import { User } from '../context/AuthContext';
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

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

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

  formData.append('file', data.videoFile);
  formData.append('user_id', data.userId.toString());
  formData.append('body_part_id', data.bodyPartId.toString());

  try {
    await apiClient.post(`/exercise_video/upload_video/${data.exerciseId}`, formData, {
      headers: {
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


interface UserExerciseVideo {
  id: number;
  video_path: string;
  create_at: string;
}

export interface UserExercise {
  id: number;
  exercise_name: string;
  description: string | null;
  body_part_name: string;
  videos: UserExerciseVideo[];
}

export const getMyExercises = async (): Promise<UserExercise[]> => {
  try {
    const response = await apiClient.get<UserExercise[]>('/exercise/my_exercises');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Błąd podczas pobierania ćwiczeń");
    }
    throw new Error("Nie można pobrać ćwiczeń. Sprawdź połączenie.");
  }
};

export const deleteExercise = async (exerciseId: number): Promise<void> => {
  try {
    await apiClient.delete(`/exercise/${exerciseId}`);
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Błąd podczas usuwania ćwiczenia");
    }
    throw new Error("Nie można usunąć ćwiczenia. Sprawdź połączenie.");
  }
};


interface ExerciseTrainer {
  first_name: string;
  last_name: string;
}

export interface ExerciseWithTrainer {
  id: number;
  exercise_name: string;
  user: ExerciseTrainer;
}


export const getExercisesByBodyPart = async (bodyPartId: number): Promise<ExerciseWithTrainer[]> => {
  try {
    const response = await apiClient.get<ExerciseWithTrainer[]>(`/exercise/by-body-part/${bodyPartId}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Błąd podczas pobierania ćwiczeń");
    }
    throw new Error("Nie można pobrać ćwiczeń dla tej partii ciała.");
  }
};


export const uploadProfileImage = async (file: File): Promise<User> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await apiClient.post<User>('/users/upload-profile-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Błąd podczas wysyłania zdjęcia");
    }
    throw new Error("Nie można było wysłać pliku. Sprawdź połączenie.");
  }
};



interface ChangePasswordData {
  old_password: string;
  new_password: string;
  confirm_password: string;
}


export const changePassword = async (data: ChangePasswordData): Promise<void> => {
  try {
    await apiClient.post('/auth/change-password', data);
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Błąd podczas zmiany hasła");
    }
    throw new Error("Nie można było zmienić hasła. Sprawdź połączenie.");
  }
};

export interface ExerciseDetails {
  id: number;
  exercise_name: string;
  description: string | null;
  video_path: string | null;
}

export const getExerciseDetails = async (exerciseId: number): Promise<ExerciseDetails> => {
  try {
    const response = await apiClient.get<ExerciseDetails>(`/exercise/${exerciseId}/details`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "Błąd podczas pobierania szczegółów ćwiczenia");
    }
    throw new Error("Nie można pobrać danych ćwiczenia.");
  }
};