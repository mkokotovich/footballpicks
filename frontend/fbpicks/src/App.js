import React, {Component} from 'react';
import { Row, Col } from 'antd';

import SignIn from './SignIn';
import Home from './Home';

import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { };
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
          <Col><SignIn /></Col>
        </Row>
        <Home currentSeason="2016" currentWeek="1" />
      </div>
    );
  }
}

export default App;
