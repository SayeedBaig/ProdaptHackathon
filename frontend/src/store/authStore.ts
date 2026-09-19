import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  setAuth: (token: string, user: User) => void;
  logout: () => void;
}

// Persist token safely with try/catch
const TOKEN_KEY = 'pitchpilot_jwt_token';
const USER_KEY = 'pitchpilot_user';

function getInitialState(): { token: string | null; user: User | null } {
  try {
    const isMock = import.meta.env.VITE_USE_MOCKS === 'true';
    if (isMock) {
      return {
        token: 'mock-jwt-token-demo-founder',
        user: {
          id: '00000000-0000-0000-0000-000000000001',
          email: 'founder@hyperscale.ai',
          name: 'Alex Vance',
        },
      };
    }
    const token = localStorage.getItem(TOKEN_KEY);
    const userJson = localStorage.getItem(USER_KEY);
    const user = userJson ? JSON.parse(userJson) : null;
    return { token, user };
  } catch {
    return { token: null, user: null };
  }
}

const initial = getInitialState();

export const useAuthStore = create<AuthState>((set) => ({
  token: initial.token,
  user: initial.user,
  isAuthenticated: !!initial.token,

  setAuth: (token: string, user: User) => {
    try {
      localStorage.setItem(TOKEN_KEY, token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    } catch {
      // Ignore localStorage errors
    }
    set({ token, user, isAuthenticated: true });
  },

  logout: () => {
    try {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    } catch {
      // Ignore
    }
    set({ token: null, user: null, isAuthenticated: false });
  },
}));
