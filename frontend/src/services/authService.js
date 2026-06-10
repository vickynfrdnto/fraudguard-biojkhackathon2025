import api from "../api/client";

export const authService = {
  login: (payload) => api.post("/auth/login", payload).then((res) => res.data),
  register: (payload) => api.post("/auth/register", payload).then((res) => res.data),
  forgotPassword: (payload) => api.post("/auth/forgot-password", payload).then((res) => res.data),
  resetPassword: (payload) => api.post("/auth/reset-password", payload).then((res) => res.data),
  verifyEmail: (payload) => api.post("/auth/verify-email", payload).then((res) => res.data),
  logout: () => api.post("/auth/logout").then((res) => res.data)
};
