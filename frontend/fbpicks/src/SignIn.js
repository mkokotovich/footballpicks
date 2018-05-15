import React from 'react';

import SignInForm from './SignInForm'

class SignIn extends React.Component {
  constructor(props) {
    super(props);
    this.handleSignIn = this.handleSignIn.bind(this);
  }

  handleSignIn(username, password) {
    console.log(username);
    console.log(password);
  }

  render() {
    return (
      <SignInForm handleSignIn={this.handleSignIn} />
    );
  }
}

export default SignIn
