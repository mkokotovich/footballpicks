import React, { Component } from 'react';
import axios from 'axios';
import { Affix, Button, Modal, Spin, Col, Row, Tooltip } from 'antd';

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
      showPicks: (props.showPicks === undefined) ? false : props.showPicks,
      submitting: false,
      loading: false,
      user: ""
    };
  }

  handleSetPick(gameIndex, teamID) {
    const picksToSubmit = this.state.picksToSubmit;
    picksToSubmit[gameIndex] = teamID;
    this.setState({picksToSubmit: picksToSubmit});
  }

  handleShowHidePicks() {
    const newShowPicks = !this.state.showPicks;
    this.setState({showPicks: newShowPicks});
    if (this.props.handleShowPicks !== undefined) {
      this.props.handleShowPicks(newShowPicks);
    }
  }

  handleEnterSubmit() {
    const submitting = this.state.submitting;
    this.setState({submitting: !submitting,
                   showPicks: submitting});

    if (submitting) {
      this.submitPicks();
    }
  }

  submitPicks() {
    this.setState({loading: true});
    const picks = this.state.games.map((game, i) => {
      return {
        "game": game.id,
        "team_to_win": this.state.picksToSubmit[i]
      };
    }).filter((pick) => {
      return pick.team_to_win !== null;
    });
    axios.post('/api/v1/picks/', picks)
      .then((response) => {
        console.log(response);
        this.setState({games: []});
        this.retrieveGames();
      })
      .catch((error) => {
        console.log(error);
        this.setState({loading: false});
        Modal.error({
          title: "Unable to submit picks",
          content: "Unable to submit your picks. Please try again\n\n" + error,
          maskClosable: true,
        })
      });
  }

  handleCancelPicks() {
    this.setState({submitting: false,
                   showPicks: false});
  }
  
  isEmpty(ob) {
    for(var i in ob) {
      return false;
    }
    return true;
  }

  render() {
    const showPicksText = this.state.showPicks ? "Hide Picks" : "Show Picks";
    const enterSubmitText = this.state.submitting ? "Submit your picks" : "Enter your picks";
    const enterSubmitButton = this.isEmpty(this.props.signedInUser) ? (
      <Tooltip title="Sign in to submit picks">
        <Button
          className="TopRightButton"
          type="primary"
          disabled="true"
          onClick={this.handleEnterSubmit}>
            {enterSubmitText}
        </Button>
      </Tooltip>
    ) : (
      <Button
        className="TopRightButton"
        type="primary"
        onClick={this.handleEnterSubmit}>
          {enterSubmitText}
      </Button>
    );
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
              { enterSubmitButton }
            </div>
            </Affix>
          </Col>
        </Row>
        <Row type="flex" justify="center">
          <Col>
            { this.state.loading && <Spin size="large" /> }
          </Col>
        </Row>
        {this.state.games.map((game, i) => <Game game={game}
                                                 key={i}
                                                 gameID={i}
                                                 display_picks={this.state.showPicks}
                                                 selectedTeam={this.state.picksToSubmit[i]}
                                                 handleSetPick={this.handleSetPick}
                                                 submitting={this.state.submitting} />)}
      </div>
    );
  }

  retrieveGames() {
    this.setState({loading: true});
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
        this.setState({loading: false});
        this.setState({ "games": games });
        this.setState({ "picksToSubmit": Array(this.state.games.length).fill(null) });
      })
      .catch((error) => {
        console.log(error);
        this.setState({loading: false});
        Modal.error({
          title: "Unable to load games",
          content: "Unable to load games. Please try again.\n\n" + error,
          maskClosable: true,
        })
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
