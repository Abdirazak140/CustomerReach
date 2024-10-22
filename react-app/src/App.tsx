import { Component, ChangeEvent, FormEvent } from "react";
import Cookies from "universal-cookie";
import 'bootstrap/dist/css/bootstrap.min.css';

const cookies = new Cookies();

interface AppState {
  username: string;
  password: string;
  error: string;
  isAuthenticated: boolean;
}

class App extends Component<{}, AppState> {
  constructor(props: {}) {
    super(props);

    this.state = {
      username: "",
      password: "",
      error: "",
      isAuthenticated: false,
    };
  }

  componentDidMount = () => {
    this.getSession();
  };

  // Get Session Method
  getSession = () => {
    fetch("/api/session/", {
      credentials: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        this.setState({ isAuthenticated: data.isAuthenticated });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  //Who Am I method
  whoami = () => {
    fetch("/api/whoami/", {
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("You are logged in as: " + data.username);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    this.setState({ password: event.target.value });
  };

  handleUserNameChange = (event: ChangeEvent<HTMLInputElement>) => {
    this.setState({ username: event.target.value });
  };

  isResponseOk = (response: Response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error(response.statusText);
    }
  };

  login = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    fetch("/api/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": cookies.get("csrftoken"),
      },
      credentials: "same-origin",
      body: JSON.stringify({
        username: this.state.username,
        password: this.state.password,
      }),
    })
      .then(this.isResponseOk)
      .then((data) => {
        console.log(data);
        this.setState({
          isAuthenticated: true,
          username: "",
          password: "",
          error: "",
        });
      })
      .catch((err) => {
        console.log(err);
        this.setState({ error: "Wrong username or password." });
      });
  };

  //Logout Method
  logout = () => {
    fetch("/api/logout", {
      credentials: "same-origin",
    })
      .then(this.isResponseOk)
      .then((data) => {
        console.log(data);
        this.setState({ isAuthenticated: false });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  render() {
    if (!this.state.isAuthenticated) {
      return (
        <div className="container mt-3">
          <h1>React Cookie Auth</h1>
          <br />
          <h2>Login</h2>
          <form onSubmit={this.login}>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                className="form-control"
                id="username"
                name="username"
                value={this.state.username}
                onChange={this.handleUserNameChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                className="form-control"
                id="password"
                name="password"
                value={this.state.password}
                onChange={this.handlePasswordChange}
              />
              <div>
                {this.state.error && (
                  <small className="text-danger">{this.state.error}</small>
                )}
              </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Login
            </button>
          </form>
        </div>
      );
    }

    return (
      <div className="container mt-3">
        <h1>React Cookie Auth</h1>
        <p>You are logged in!</p>
        <button className="btn btn-primary mr-2" onClick={this.whoami}>
          WhoAmI
        </button>
        <button className="btn btn-danger" onClick={this.logout}>
          Log out
        </button>
      </div>
    );
  }
}

export default App;
