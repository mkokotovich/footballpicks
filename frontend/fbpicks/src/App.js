import React, {Component} from 'react';
import { Row, Col } from 'antd';

import SignIn from './SignIn';
import Home from './Home';

import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null
    };
  }

  handleAuthChange = (user) => {
    this.setState({
      user: user,
    });
  }

  render() {
    return (
      <div className="App">
        <Row
          type="flex"
          justify="space-between"
          className="navbar"
          align="middle"
          >
          <Col className="Logo">Football Picks</Col>
          <Col><SignIn handleAuthChange={this.handleAuthChange} /></Col>
        </Row>
        <Home currentSeason="2018" currentWeek="1" signedInUser={this.state.user} />
      </div>
    );
  }
}

export default App;
