import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { mockApi } from '../services/mockApi';

// Add prop type for setIsAuthenticated
interface DashboardPageProps {
  setIsAuthenticated: (value: boolean) => void;
}

export const DashboardPage = ({ setIsAuthenticated }: DashboardPageProps) => {
  const navigate = useNavigate();

  const handleWhoAmI = async () => {
    try {
      const data = await mockApi.whoami();
      console.log("You are logged in as: " + data.username);
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogout = async () => {
    try {
      await mockApi.logout();
      // Update authentication state
      setIsAuthenticated(false);
      navigate('/login');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      <p className="mb-4">You are logged in!</p>
      <div className="space-x-4">
        <button
          onClick={handleWhoAmI}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          WhoAmI
        </button>
        <button
          onClick={handleLogout}
          className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
        >
          Log out
        </button>
      </div>
    </div>
  );
};