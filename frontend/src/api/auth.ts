import axios from "axios";

const API_URL = "http://localhost:8080/auth"; // zakładam, że backend działa na porcie 8000

export const register = async (data: any) => {
  return await axios.post(`${API_URL}/register`, data);
};

export const login = async (data: any) => {
  return await axios.post(`${API_URL}/login`, data);
};
