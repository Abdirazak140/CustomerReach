// services/mockApi.ts
export const mockApi = {
    login(data: { username: string; password: string }) {
      // Simple mock authentication
      if (data.username === 'testuser' && data.password === 'password') {
        // Simulate successful login
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('username', data.username);
        return Promise.resolve({ username: data.username });
      }
      // Simulate login failure
      return Promise.reject(new Error('Invalid credentials'));
    },
  
    logout() {
      // Clear authentication state
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('username');
      return Promise.resolve();
    },
  
    getSession() {
      // Check if user is authenticated
      const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
      return Promise.resolve({ 
        isauthenticated: isAuthenticated,
        username: isAuthenticated ? localStorage.getItem('username') : null 
      });
    },
  
    whoami() {
      // Return mock user info if authenticated
      const username = localStorage.getItem('username');
      return username 
        ? Promise.resolve({ username }) 
        : Promise.reject(new Error('Not authenticated'));
    }
  };
  