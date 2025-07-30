import React from "react";


interface InputProps {
    label: string;
    name: string;
    type?: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
    error?: string;
}
  
const Input: React.FC<InputProps> = ({
label,
type = "text",
name,
value,
onChange,
error,
}) => (
<div className="flex flex-col mb-4">
    <label className="mb-1 font-semibold text-white text-sm tracking-wide">{label}</label>
    <input
    type={type}
    name={name}
    value={value}
    onChange={onChange}
    className={`p-2 border ${error ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400`}
    />
    {error && <span className="text-red-500 text-xs">{error}</span>}
</div>
);
export default Input;