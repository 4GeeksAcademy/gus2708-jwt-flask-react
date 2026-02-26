class Actions {
  constructor(state, dispatch) {
    this.state = state;
    this.dispatch = dispatch;
  };

  async login(email, password) {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      const data = await response.json();

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user_email", email);

      this.dispatch({ type: "SET_JWT", payload: data.access_token });
      this.dispatch({ type: "SET_USER", payload: { email: email } });

      return true;
    } else {
      const errorData = await response.json();
      console.error("Login fallido:", errorData.error);
      return false;
    };
  };

  async register(email, password) {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    return response.ok;
  };

  async logout() {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/logout`, {
      method: 'POST',
      headers: { 
        'Authorization': `Bearer ${this.state.jwt}` 
      }
    });

    if (response.ok) {
      localStorage.removeItem("token");

      this.dispatch({ type: 'UNSET_USER' });
    };
  };
}

export default Actions;
