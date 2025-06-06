import axios from "axios";

const API_URL = "http://localhost:8080/auth"; 

export const register = async (data: any) => {
  return await axios.post(`${API_URL}/register`, data);
};

export const login = async (data: any) => {
  return await axios.post(`${API_URL}/login`, data);
};

export const userData = async (data: any) => {
  return await axios.get(`${API_URL}/users/me`, data);
};

export const logout = async (token: string) => {
  return await axios.post(
    `${API_URL}/logout`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};

