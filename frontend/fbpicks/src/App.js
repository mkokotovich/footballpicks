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

  getCurrentSeason = () => {
    const now = new Date();
    const currentMonth = now.getMonth()+1; //January is 0!
    const currentYear = now.getFullYear();

    if (currentMonth < 3) {
      return (currentYear - 1);
    } else {
      return currentYear;
    }
  }

  // This is ugly, but not sure if there is a better way
  getWeek1StartForSeason = (season) => {
    // Date months are 0-indexed, 8==sept
    if (season === 2015) {
        return new Date(2015,8,8);
    } else if (season === 2016) {
        return new Date(2016,8,6);
    } else if (season === 2017) {
        return new Date(2017,8,5);
    } else if (season === 2018) {
        return new Date(2018,8,4);
    }
    return new Date(2015,8,8);

  }

  getCurrentWeek = () => {
    const now = new Date();
    const week1Start = this.getWeek1StartForSeason(this.getCurrentSeason());
    console.log("now: " + now + " week1: " + week1Start);
    if (now < week1Start) {
      return 1;
    }
    const tdelta = now - week1Start;
    const week = Math.ceil((tdelta/(60*60*24))/7);
    return week > 17 ? 17 : week;
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
        <Home currentSeason={this.getCurrentSeason().toString()} currentWeek={this.getCurrentWeek().toString()} signedInUser={this.state.user} />
      </div>
    );
  }
}

export default App;
