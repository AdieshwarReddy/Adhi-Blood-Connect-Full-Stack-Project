import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { AuthAPI, DonorsAPI } from "@/services/api";
import { toast } from "sonner";

export type Role = "donor" | "patient" | "hospital" | "admin";

export interface User {
  id: string;
  name: string;
  email: string;
  role: Role;
  bloodGroup?: string;
  city?: string;
  available?: boolean;
}

interface AuthContextValue {
  user: User | null;
  login: (email: string, password: string, role: Role) => Promise<void>;
  signup: (name: string, email: string, password: string, role: Role, bloodGroup?: string) => Promise<void>;
  loginWithGoogle: (role: Role) => Promise<void>;
  logout: () => void;
  updateUser: (patch: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);
const STORAGE_KEY = "adhi_auth_user";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) setUser(JSON.parse(raw));
    } catch {}
  }, []);

  const persist = (u: User | null) => {
    setUser(u);
    if (u) localStorage.setItem(STORAGE_KEY, JSON.stringify(u));
    else localStorage.removeItem(STORAGE_KEY);
  };

  const login: AuthContextValue["login"] = async (email, password, role) => {
    try {
      const res = await AuthAPI.login({ email, password });
      const { accessToken, user: dbUser } = res.data.data;
      localStorage.setItem("adhi_jwt", accessToken);
      persist({
        id: dbUser.id,
        name: dbUser.name,
        email: dbUser.email,
        role: dbUser.role as Role,
        bloodGroup: dbUser.blood_group,
        city: dbUser.city,
        available: dbUser.availability,
      });
    } catch (error: any) {
      const message = error.response?.data?.message || "Invalid email or password.";
      toast.error(message);
      throw error;
    }
  };

  const signup: AuthContextValue["signup"] = async (name, email, password, role, bloodGroup) => {
    try {
      const res = await AuthAPI.signup({
        name,
        email,
        password,
        role,
        blood_group: bloodGroup || "O+",
        city: "Bangalore",
        phone_number: "+919876543210",
        coordinates: [77.5946, 12.9716],
        availability: true,
      });
      const { accessToken, user: dbUser } = res.data.data;
      localStorage.setItem("adhi_jwt", accessToken);
      persist({
        id: dbUser.id,
        name: dbUser.name,
        email: dbUser.email,
        role: dbUser.role as Role,
        bloodGroup: dbUser.blood_group,
        city: dbUser.city,
        available: dbUser.availability,
      });
    } catch (error: any) {
      const message = error.response?.data?.message || "Registration failed.";
      toast.error(message);
      throw error;
    }
  };

  const loginWithGoogle: AuthContextValue["loginWithGoogle"] = async (role) => {
    try {
      const res = await AuthAPI.google("dummy-google-token-123");
      const { accessToken, user: dbUser } = res.data.data;
      localStorage.setItem("adhi_jwt", accessToken);
      persist({
        id: dbUser.id,
        name: dbUser.name,
        email: dbUser.email,
        role: dbUser.role as Role,
        bloodGroup: dbUser.blood_group,
        city: dbUser.city,
        available: dbUser.availability,
      });
    } catch (error: any) {
      const message = error.response?.data?.message || "Google authentication failed.";
      toast.error(message);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem("adhi_jwt");
    persist(null);
  };

  const updateUser = async (patch: Partial<User>) => {
    if (!user) return;
    const updated = { ...user, ...patch };
    persist(updated);
    if (patch.available !== undefined) {
      try {
        await DonorsAPI.updateAvailability(patch.available);
      } catch (err) {
        console.error("Failed to update availability on backend:", err);
      }
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, loginWithGoogle, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
