import React, {Component} from 'react';
import { Route, Redirect, Link } from 'react-router-dom';
import { Row, Col } from 'antd';

import SignIn from './SignIn';
import Home from './Home';
import Records from './Records';

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
  // Week 1 start should be the Tuesday after Labor Day
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
    } else if (season === 2019) {
        return new Date(2019,8,3);
    } else if (season === 2020) {
        return new Date(2020,8,7);
    } else if (season === 2021) {
        return new Date(2021,8,6);
    } else if (season === 2022) {
        return new Date(2022,8,5);
    } else if (season === 2023) {
        return new Date(2023,8,5);
    } else if (season === 2024) {
        return new Date(2024,8,3);
    } else if (season === 2025) {
        return new Date(2025,8,2);
    } else if (season === 2026) {
        return new Date(2026,8,8);
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
    const week = Math.ceil(((tdelta/1000)/(60*60*24))/7);
    console.log("tdelta: " + tdelta + " week: " + week);
    return week > 18 ? 18 : week;
  }

  render() {
    const currentSeason = this.getCurrentSeason().toString();
    const currentWeek = this.getCurrentWeek().toString();

    return (
      <div className="App">
        <Row
          type="flex"
          justify="space-between"
          className="navbar"
          align="middle"
          >
          <Col className="Logo"><Link to="/" style={{ textDecoration: "none", color: '#663300' }}>Football Picks</Link></Col>
          <Col><SignIn handleAuthChange={this.handleAuthChange} /></Col>
        </Row>
        <Route
          exact
          path="/"
          render={() => {
            return <Redirect to={`/games/${currentSeason}/${currentWeek}`}/>
          }}
        />
        <Route
          exact
          path="/records"
          render={() => {
            return <Records currentSeason={this.getCurrentSeason().toString()} currentWeek={this.getCurrentWeek().toString()} signedInUser={this.state.user} />;
          }}
        />
        <Route
          exact
          path="/games"
          render={() => {
            console.log(`Matched /games, redirecting to /games/${currentSeason}/${currentWeek}`);
            return <Redirect to={`/games/${currentSeason}/${currentWeek}`}/>
          }}
        />
        <Route
          exact
          path="/games/:season"
          render={({ match }) => {
            console.log(`Matched /games/${match.params.season}, redirecting to /games/${match.params.season}/${currentWeek}`);
            return <Redirect to={`/games/${match.params.season}/${currentWeek}`}/>
          }}
        />
        <Route
          path="/games/:season/:week"
          render={({ match }) => {
            console.log(`Matched /games/${match.params.season}/${match.params.week}, returning Home with season=${match.params.season} and week=${match.params.week}`);
            return <Home currentSeason={this.getCurrentSeason().toString()} currentWeek={this.getCurrentWeek().toString()} season={match.params.season} week={match.params.week} signedInUser={this.state.user} />;
          }}
        />
      </div>
    );
  }
}

export default App;
