import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

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

  const login: AuthContextValue["login"] = async (email, _password, role) => {
    const u: User = {
      id: crypto.randomUUID(),
      name: email.split("@")[0] || "User",
      email,
      role,
      bloodGroup: "O+",
      city: "Bangalore",
      available: true,
    };
    persist(u);
  };

  const signup: AuthContextValue["signup"] = async (name, email, _password, role, bloodGroup) => {
    persist({
      id: crypto.randomUUID(),
      name,
      email,
      role,
      bloodGroup: bloodGroup || "O+",
      city: "Bangalore",
      available: true,
    });
  };

  const loginWithGoogle: AuthContextValue["loginWithGoogle"] = async (role) => {
    persist({
      id: crypto.randomUUID(),
      name: "Google User",
      email: "google.user@gmail.com",
      role,
      bloodGroup: "A+",
      city: "Mumbai",
      available: true,
    });
  };

  const logout = () => persist(null);
  const updateUser = (patch: Partial<User>) => {
    if (!user) return;
    persist({ ...user, ...patch });
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
