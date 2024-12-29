import Cookies from 'universal-cookie';
import { LoginFormData } from '../types/auth.types';

const cookies = new Cookies();

const BASE_URL = '/api/auth';

export const api = {
  async getSession() {
    const response = await fetch(`${BASE_URL}/session/`, {
      credentials: 'same-origin',
    });
    return response.json();
  },

  async login(data: LoginFormData) {
    const response = await fetch(`${BASE_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': cookies.get('csrftoken'),
      },
      credentials: 'same-origin',
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error('Login failed');
    }
    return response.json();
  },

  async logout() {
    const response = await fetch(`${BASE_URL}/logout/`, {
      credentials: 'same-origin',
    });
    return response.json();
  },

  async whoami() {
    const response = await fetch(`${BASE_URL}/whoami/`, {
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin',
    });
    return response.json();
  },
};