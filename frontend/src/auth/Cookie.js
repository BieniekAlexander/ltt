import React from 'react';
import {ReactSession} from 'react-client-session';

class Cookie extends React.Component {
  constructor() {
    super(); 
    this.state = {
      username: "",
      sessionUsername: ""
    }
    this.setUsername = this.setUsername.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.clear = this.clear.bind(this);

    ReactSession.setStoreType("cookie");
  }

  setUsername(event) {
    event.preventDefault();
    ReactSession.set("username", this.state.username);

    this.setState({
      sessionUsername: "User Name is: " + ReactSession.get("username")
    });
  }

  clear(event) {
    event.preventDefault();
    ReactSession.remove("username");

    this.setState({
      sessionUsername: "User Name is: " + ReactSession.get("username"),
      message: "Cookie cleared!"
    });
  }

  handleChange(event) {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({
      [name]: value,
    });
  }

  render() {
    return (<div>
        <p>{this.state.sessionUsername}</p>

        <h3>Client Session store with cookie persistence</h3>

        <p>Add a username and display it  <Link to="/">Back</Link></p>

        <input type="text" name="username" value={this.state.username} onChange={this.handleChange} placeholder="Set a username" />
        <button type="submit" onClick={this.setUsername}>Add to Session(cookie)</button>

        <p>{this.state.sessionUsername}</p>

        <button type="submit" disabled={this.state.sessionUsername === ""} onClick={this.clear}>Clear cookie</button>
        {this.state.message}
      </div>
    )
  }
}