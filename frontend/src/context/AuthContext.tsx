import { createContext, useState, ReactNode } from "react";

interface AuthContextType {
  user: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<string | null>(null);

  const login = async (email: string, password: string) => {
    // 실제 로그인 API 호출 부분 (백엔드와 연동 필요)
    console.log("로그인 요청:", email, password);
    setUser(email);
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
