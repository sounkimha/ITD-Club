ㅑㅡㅔ
interface InputFieldProps {
    label: string;
    type: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  }
  
  export const InputField = ({ label, type, value, onChange }: InputFieldProps) => (
    <div>
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <input 
        type={type} 
        value={value} 
        onChange={onChange} 
        className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
  );
  