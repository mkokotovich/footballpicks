import React, { Component } from 'react';
import axios from 'axios';
import { Affix, Button, Modal, Spin, Col, Row, Tooltip } from 'antd';
import { withRouter } from 'react-router-dom';

import './GameList.css';

import Game from './Game';

function GameListWeekMessage(props) {
  return (
    <Row type="flex" justify="start" align="bottom">
      <Col xs={24} sm={{push: 2}} md={{push: 4}}>
        <span className="GameListWeekMessage">Games for Week {props.week}, {props.season}</span>
      </Col>
    </Row>
  );
}

class GameList extends Component {
  constructor(props) {
    super(props);
    this.handleShowHidePicks = this.handleShowHidePicks.bind(this);
    this.handleShowHideScores = this.handleShowHideScores.bind(this);
    this.handleEnterSubmit = this.handleEnterSubmit.bind(this);
    this.handleCancelPicks = this.handleCancelPicks.bind(this);
    this.handleSetPick = this.handleSetPick.bind(this);
    this.state = {
      games: [],
      picksToSubmit: [],
      showPicks: (props.showPicks === undefined) ? false : props.showPicks,
      showScores: (props.showScores === undefined) ? false : props.showScores,
      submitting: false,
      loading: false,
      refreshing: false,
      scoresAvailable: false
    };
  }

  componentDidMount() {
      this.retrieveGames();
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps.season !== this.props.season || prevProps.week !== this.props.week) {
      this.retrieveGames();
    } else if (this.props.signedInUser &&
      (!prevProps.signedInUser || prevProps.signedInUser.id !== this.props.signedInUser.id)) {
      this.loadInitialPicksForUser();
    }
  }

  handleSetPick(gameIndex, teamID) {
    const picksToSubmit = this.state.picksToSubmit;
    picksToSubmit[gameIndex] = teamID;
    this.setState({picksToSubmit: picksToSubmit});
  }

  loadInitialPicksForUser() {
    if (this.props.signedInUser === null) {
      return;
    }
    const picksToSubmit = this.state.games.map((game, i) => {
      const user_pick = game.picks.filter((pick) => {
        if (pick.user.id === this.props.signedInUser.id) {
          return true;
        }
        return false;
      });
      if (user_pick.length > 0) {
        return user_pick[0].team_to_win;
      } else {
        return null;
      }
    });
    this.setState({picksToSubmit: picksToSubmit});
  }

  handleShowHidePicks() {
    const newShowPicks = !this.state.showPicks;
    this.setState({showPicks: newShowPicks});
    if (this.props.handleShowPicks !== undefined) {
      this.props.handleShowPicks(newShowPicks);
    }
  }

  handleShowHideScores() {
    const newShowScores = !this.state.showScores;
    this.setState({showScores: newShowScores});
  }

  handleEnterSubmit() {
    const submitting = this.state.submitting;

    if (submitting) {
      this.submitPicks();
    } else {
      this.setState({submitting: true,
                     showPicks: false,
                     showScores: false});
    }
  }

  submitPicks() {
    const picks = this.state.games.map((game, i) => {
      return {
        "game": game.id,
        "team_to_win": this.state.picksToSubmit[i]
      };
    }).filter((pick) => {
      return pick.team_to_win !== null;
    });
    if (picks.length === 0) {
      Modal.error({
        title: "Empty selection",
        content: "Select who you think will win by clicking the checkbox next to the team name.",
        maskClosable: true,
      })
      return;
    }
    const missingPicks = this.state.games.length - picks.length;
    this.setState({loading: true});
    axios.post('/api/v1/picks/', picks)
      .then((response) => {
        console.log(response);
        this.setState({games: []});
        this.retrieveGames();
        this.setState({submitting: false,
                       showPicks: true});
        if (missingPicks !== 0) {
          Modal.info({
            title: "Some games missing picks",
            content: `${picks.length} picks submitted successfully, but ${missingPicks} games do not have picks selected`,
            maskClosable: true,
          });
        }
      })
      .catch((error) => {
        const errorString = error.response ? error.response.data : error;
        console.log(errorString);
        this.setState({loading: false});
        Modal.error({
          title: "Unable to submit picks",
          content: "Unable to submit your picks. Please try again\n\n" + errorString,
          maskClosable: true,
        })
      });
  }

  handleCancelPicks() {
    this.setState({submitting: false,
                   showPicks: false});
  }
  
  render() {
    const showPicksText = this.state.showPicks ? "Hide Picks" : "Show Picks";
    const showScoresText = this.state.showScores ? "Hide Scores" : "Show Scores";
    const enterSubmitText = this.state.submitting ? "Submit your picks" : "Enter your picks";
    const refreshScoresButton = (
      <Button
        className="TopRightButton"
        onClick = {() => {
          this.setState({refreshing: true});
          this.retrieveScores()
        }} >
          Refresh scores
      </Button>
    );
    const showHideScoresButton = !this.state.scoresAvailable ? (
      <Tooltip title="Game scores are currently not available">
        <Button
          className="TopRightButton"
          disabled="true"
          onClick={this.handleShowHideScores}>
            {showScoresText}
        </Button>
      </Tooltip>
    ) : (
      <Button
        className="TopRightButton"
        onClick={this.handleShowHideScores}>
          {showScoresText}
      </Button>
    );
    const enterSubmitButton = this.props.signedInUser === null ? (
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
        <Row type="flex" style={{ marginBottom: "15px"}} align="bottom">
          <Col xs={24} sm={14}>
            {GameListWeekMessage({week: this.props.week, season: this.props.season})}
          </Col>
          <Col xs={24} sm={10}>
            <Affix>
            <div className="AlignRight">
              { this.state.showScores &&
                refreshScoresButton
              }
              { !this.state.submitting && this.props.allowScores &&
                showHideScoresButton
              }
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
          <Col className="roundedDivider">
            &nbsp;
          </Col>
        </Row>
        <Row type="flex" justify="center">
          <Col>
            { (this.state.loading || this.state.refreshing) && <Spin size="large" /> }
          </Col>
        </Row>
        {this.state.games.map((game, i) => <Game game={game}
                                                 key={i}
                                                 gameID={i}
                                                 display_picks={this.state.showPicks}
                                                 selectedTeam={this.state.picksToSubmit[i]}
                                                 handleSetPick={this.handleSetPick}
                                                 submitting={this.state.submitting}
                                                 signedInUser={this.props.signedInUser}
                                                 showScores={this.state.showScores} />)}
      </div>
    );
  }

  retrieveGames() {
    this.setState({loading: true});
    axios.get('/api/v1/games/', {
        params: {
          season: this.props.season,
          week: this.props.week,
        }
      })
      .then((response) => {
        const games = response.data.results;
        this.setState({loading: false});
        this.setState({ "games": games });
        this.setState({ "picksToSubmit": Array(this.state.games.length).fill(null) });
        this.loadInitialPicksForUser();
        if (this.props.allowScores) {
          this.retrieveScores();
        }
      })
      .catch((error) => {
        const errorString = error.response ? error.response.data : error;
        console.log(errorString);
        this.setState({loading: false});
        Modal.error({
          title: "Unable to load games",
          content: "Unable to load games. Please try again.\n\n" + errorString,
          maskClosable: true,
        })
      });
  }

  retrieveScores() {
    axios.get('/api/v1/games/scores/')
      .then((response) => {
        this.setState({refreshing: false});
        const scores = response.data;
        const games = this.state.games.map((game, i) => {
          const score = scores.find(score => score.game_id === game.id);
          if (score !== undefined) {
            if (!this.state.scoresAvailable) {
              this.setState({"scoresAvailable": true});
            }
            game.score = score;
          }

          return game
        });
        this.setState({"games": games});
      })
      .catch((error) => {
        const errorString = error.response ? error.response.data : error;
        console.log(errorString);
        this.setState({refreshing: false});
        this.setState({
          "scoresAvailable": false
        });
      });
  }
}

GameList.defaultProps = {
    season: '2016',
    week: '1'
  };

export default withRouter(GameList);
