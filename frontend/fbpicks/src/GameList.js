import React, { Component } from 'react';
import axios from 'axios';
import { Affix, Button, Col, Row } from 'antd';

import './GameList.css';

import Game from './Game';

function GameListWeekMessage(props) {
  return (
    <span className="GameListWeekMessage">Games for Week {props.week}, {props.season}</span>
  );
}

class GameList extends Component {
  constructor(props) {
    super(props);
    this.handleShowHidePicks = this.handleShowHidePicks.bind(this);
    this.handleEnterSubmit = this.handleEnterSubmit.bind(this);
    this.handleCancelPicks = this.handleCancelPicks.bind(this);
    this.handleSetPick = this.handleSetPick.bind(this);
    this.state = {
      games: [],
      picksToSubmit: [],
      showPicks: false,
      submitting: false
    };
  }

  handleSetPick(gameIndex, teamID) {
    const picksToSubmit = this.state.picksToSubmit;
    picksToSubmit[gameIndex] = teamID;
    this.setState({picksToSubmit: picksToSubmit});
  }

  handleShowHidePicks() {
    this.setState({showPicks: !this.state.showPicks});
  }

  handleEnterSubmit() {
    this.setState({submitting: !this.state.submitting,
                   showPicks: this.state.submitting});
  }

  handleCancelPicks() {
    this.setState({submitting: false,
                   showPicks: false});
  }

  render() {
    const showPicksText = this.state.showPicks ? "Hide Picks" : "Show Picks";
    const enterSubmitText = this.state.submitting ? "Submit your picks" : "Enter your picks";
    return (
      <div className="GameList">
        <Row type="flex">
          <Col xs={24} sm={14}>
            {GameListWeekMessage(this.props)}
          </Col>
          <Col xs={24} sm={10}>
            <Affix>
            <div className="AlignRight">
              { this.state.submitting && 
                <Button
                  className="TopRightButton"
                  onClick={this.handleCancelPicks}>
                    Cancel
                </Button>
              }
              { !this.state.submitting && 
                <Button
                  className="TopRightButton"
                  onClick={this.handleShowHidePicks}>
                    {showPicksText}
                </Button>
              }
              <Button
                className="TopRightButton"
                type="primary"
                onClick={this.handleEnterSubmit}>
                  {enterSubmitText}
              </Button>
            </div>
            </Affix>
          </Col>
        </Row>
        {this.state.games.map((game, i) => <Game game={game}
                                                 key={i}
                                                 gameID={i}
                                                 display_picks={this.state.showPicks}
                                                 selected={this.state.picksToSubmit.length > 0 ? this.state.picksToSubmit[i] : false}
                                                 handleSetPick={this.handleSetPick}
                                                 submitting={this.state.submitting} />)}
      </div>
    );
  }

  retrieveGames() {
    /* Special workaround for funny DB entries for season 2015 */
    const season = this.props.season === 2015 ? 0 : this.props.season;
    axios.get('/api/v1/games/', {
        params: {
          season: season,
          week: this.props.week,
        }
      })
      .then((response) => {
        const games = response.data.results;
        this.setState({ "games": games });
        this.setState({ "picksToSubmit": Array(this.state.games.length).fill(false) });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  componentDidMount() {
    this.retrieveGames();
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps.season !== this.props.season) {
      this.retrieveGames();
    }
    if (prevProps.week !== this.props.week) {
      this.retrieveGames();
    }
  }
}

GameList.defaultProps = {
    season: '2016',
    week: '1'
  };

export default GameList;
