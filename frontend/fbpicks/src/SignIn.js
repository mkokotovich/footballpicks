import React from 'react';
import { Button } from 'antd';

import SignInForm from './SignInForm'

function SignOut(props) {
  return (
    <Button 
      type="primary"
      onClick={props.handleSignOut}>
      Sign Out
    </Button>
  );
}

class SignIn extends React.Component {
  constructor(props) {
    super(props);
    this.handleSignIn = this.handleSignIn.bind(this);
    this.handleSignOut = this.handleSignOut.bind(this);
    this.state = {
      isSignedIn: false
    };
  }

  handleSignIn(username, password) {
    console.log("Signed in: " + username);
    this.setState({isSignedIn: true});
  }

  handleSignOut() {
    console.log("Signed out");
    this.setState({isSignedIn: false});
  }

  render() {
    const signInOrOut = this.state.isSignedIn ? (
      <SignOut handleSignOut={this.handleSignOut} />
    ) : (
      <SignInForm handleSignIn={this.handleSignIn} />
    );

    return (
      <div className="SignIn">
        {signInOrOut}
      </div>
    );
  }
}

export default SignIn
