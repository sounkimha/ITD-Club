import { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { InputField } from "./InputField";
import { Button } from "@/components/ui/button";

const LoginForm = () => {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("모든 필드를 입력해주세요.");
      return;
    }

    try {
      await login(email, password);
    } catch (err) {
      setError("로그인 실패. 이메일 또는 비밀번호를 확인해주세요.");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-bold mb-4 text-center">로그인</h2>
      {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <InputField 
          label="이메일" 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
        />
        <InputField 
          label="비밀번호" 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        <Button type="submit" className="w-full">로그인</Button>
      </form>
    </div>
  );
};

export default LoginForm;
