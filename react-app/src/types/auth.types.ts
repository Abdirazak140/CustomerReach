export interface AuthState {
    username: string;
    password: string;
    error: string;
    isAuthenticated: boolean;
  }
  
  export interface LoginFormData {
    username: string;
    password: string;
  }