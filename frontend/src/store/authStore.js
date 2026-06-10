import { create } from "zustand";

export const useAuthStore = create((set) => ({
  accessToken: localStorage.getItem("fg_access_token"),
  refreshToken: localStorage.getItem("fg_refresh_token"),
  setTokens: (accessToken, refreshToken) => {
    localStorage.setItem("fg_access_token", accessToken);
    localStorage.setItem("fg_refresh_token", refreshToken);
    set({ accessToken, refreshToken });
  },
  logout: () => {
    localStorage.removeItem("fg_access_token");
    localStorage.removeItem("fg_refresh_token");
    set({ accessToken: null, refreshToken: null });
  }
}));
