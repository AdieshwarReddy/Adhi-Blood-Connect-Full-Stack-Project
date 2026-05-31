import axios from "axios";

// API service layer — replace baseURL with your backend.
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  headers: { "Content-Type": "application/json" },
});

// Attach JWT from localStorage if present.
api.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("adhi_jwt") : null;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Placeholder endpoints — implement on your backend.
export const AuthAPI = {
  login: (data: { email: string; password: string }) => api.post("/auth/login", data),
  signup: (data: { name: string; email: string; password: string; role: string }) =>
    api.post("/auth/signup", data),
  google: (token: string) => api.post("/auth/google", { token }),
};

export const DonorsAPI = {
  search: (params: Record<string, unknown>) => api.get("/donors", { params }),
  me: () => api.get("/donors/me"),
  updateAvailability: (available: boolean) => api.patch("/donors/me", { available }),
};

export const RequestsAPI = {
  list: () => api.get("/requests"),
  create: (data: unknown) => api.post("/requests", data),
};

export const ChatAPI = {
  ask: (message: string) => api.post("/chat", { message }),
};
