import axios from "axios";
import { useAuthStore } from "../store/authStore";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  timeout: 15000
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    const { refreshToken, setTokens, logout } = useAuthStore.getState();
    if (error.response?.status === 401 && refreshToken && !original._retry) {
      original._retry = true;
      try {
        const response = await axios.post(`${api.defaults.baseURL}/auth/refresh`, { refresh_token: refreshToken });
        setTokens(response.data.access_token, response.data.refresh_token);
        original.headers.Authorization = `Bearer ${response.data.access_token}`;
        return api(original);
      } catch (refreshError) {
        logout();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
