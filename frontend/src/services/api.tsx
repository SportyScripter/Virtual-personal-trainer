
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