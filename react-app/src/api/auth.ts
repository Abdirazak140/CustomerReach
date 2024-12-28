import Cookies from "universal-cookie";

const cookies = new Cookies();

export const getSession = async () => {
  const response = await fetch("/api/auth/session/", {
    credentials: "same-origin",
  });
  return response.json();
};

export const whoami = async () => {
  const response = await fetch("/api/auth/whoami/", {
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "same-origin",
  });
  return response.json();
};

export const login = async (username: string, password: string) => {
  const response = await fetch("/api/auth/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": cookies.get("csrftoken"),
    },
    credentials: "same-origin",
    body: JSON.stringify({ username, password }),
  });
  
  if (!response.ok) {
    throw new Error("Invalid credentials");
  }
  
  return response.json();
};

export const logout = async () => {
  const response = await fetch("/api/auth/logout/", {
    credentials: "same-origin",
  });
  
  if (!response.ok) {
    throw new Error("Logout failed");
  }
  
  return response.json();
};