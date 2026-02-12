import React from 'react';
import { cn } from '../../lib/utils';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';

const Input = React.forwardRef(({ className, type, placeholder, label, error, icon: Icon, value, onChange, ...props }, ref) => {
  const [showPassword, setShowPassword] = React.useState(false);

  const getType = () => {
    if (type === 'password' && showPassword) return 'text';
    return type;
  };

  const getIcon = () => {
    if (type === 'password') {
      return (
        <button
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
        >
          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
        </button>
      );
    }
    if (Icon) {
      return <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 group-hover:text-blue-500"><Icon size={16} /></div>;
    }
    return null;
  };

  return (
    <div className="flex flex-col gap-1 w-full relative group">
      {label && <label className="text-sm font-medium text-gray-700 dark:text-gray-300 ml-1">{label}</label>}
      <div className="relative">
        <input
          type={getType()}
          className={cn(
            "flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:ring-offset-gray-900 dark:placeholder:text-gray-400",
            Icon && "pl-10",
            type === 'password' && "pr-10",
            error && "border-red-500 focus-visible:ring-red-500",
            className
          )}
          placeholder={placeholder}
          ref={ref}
          value={value}
          onChange={onChange}
          {...props}
        />
        {getIcon()}
      </div>
      {error && <p className="text-xs text-red-500 ml-1">{error}</p>}
    </div>
  );
});

Input.displayName = "Input";

export { Input };
