import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import { authService } from "../services/authService";
import { useAuthStore } from "../store/authStore";

export default function LoginPage() {
  const accessToken = useAuthStore((state) => state.accessToken);
  const setTokens = useAuthStore((state) => state.setTokens);
  const [form, setForm] = useState({ email: "", password: "" });
  const [mode, setMode] = useState("login");
  const [error, setError] = useState("");

  if (accessToken) return <Navigate to="/" replace />;

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const response = mode === "login"
        ? await authService.login(form)
        : await authService.register({ ...form, full_name: form.email.split("@")[0] || "FraudGuard User" });
      setTokens(response.access_token, response.refresh_token);
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <form onSubmit={submit} className="bg-white rounded-lg shadow p-6 w-full max-w-sm space-y-4">
        <div className="flex items-center space-x-2 text-indigo-800">
          <i className="fas fa-shield-alt text-2xl"></i>
          <h1 className="text-xl font-bold">FraudGuard</h1>
        </div>
        <h2 className="text-lg font-semibold text-gray-800">{mode === "login" ? "Login" : "Register"}</h2>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <input className="border rounded w-full px-3 py-2 text-sm" type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        <input className="border rounded w-full px-3 py-2 text-sm" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        <button className="bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700 w-full">
          {mode === "login" ? "Login" : "Create Account"}
        </button>
        <button type="button" className="text-sm text-indigo-700" onClick={() => setMode(mode === "login" ? "register" : "login")}>
          {mode === "login" ? "Create an account" : "Use existing account"}
        </button>
      </form>
    </div>
  );
}
