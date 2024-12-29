import { useState, ChangeEvent, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/LoginForm';
import { mockApi } from '../services/mockApi';

// Add prop type for setIsAuthenticated
interface LoginPageProps {
  setIsAuthenticated: (value: boolean) => void;
}

export const LoginPage = ({ setIsAuthenticated }: LoginPageProps) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    error: '',
  });

  const handleUsernameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, username: e.target.value }));
  };

  const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, password: e.target.value }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      // Attempt login
      const response = await mockApi.login({
        username: formData.username,
        password: formData.password,
      });
      
      // If login successful, update authentication state
      setIsAuthenticated(true);
      
      // Navigate to dashboard
      navigate('/dashboard');
    } catch (error) {
      // If login fails, show error
      setFormData(prev => ({ ...prev, error: 'Wrong username or password.' }));
      setIsAuthenticated(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Login to your account
          </h2>
        </div>
        <LoginForm
          username={formData.username}
          password={formData.password}
          error={formData.error}
          onUsernameChange={handleUsernameChange}
          onPasswordChange={handlePasswordChange}
          onSubmit={handleSubmit}
        />
      </div>
    </div>
  );
};