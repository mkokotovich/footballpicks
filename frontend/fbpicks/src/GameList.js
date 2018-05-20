import React, { Component } from 'react';
import axios from 'axios';

import './GameList.css';

import Game from './Game';

function GameListWeekMessage(props) {
  return (
    <h2>Week {props.week}, {props.season} Matchups</h2>
  );
}

class GameList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      games: []
    };
  }

  render() {
    return (
      <div className="GameList">
        {GameListWeekMessage(this.props)}
        {this.state.games.map((game, i) => <Game game={game}
                                                 key={i}
                                                 display_picks={this.props.display_picks} />)}
      </div>
    );
  }

  retrieveGames() {
    /* Special workaround for funny DB entries for season 2015 */
    const season = this.props.season == 2015 ? 0 : this.props.season;
    axios.get('/api/v1/games/', {
        params: {
          season: season,
          week: this.state.week,
        }
      })
      .then((response) => {
        const games = response.data.results;
        this.setState({ "games": games });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  componentDidMount() {
    this.retrieveGames();
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps.season != this.props.season) {
      this.retrieveGames();
    }
  }
}

GameList.defaultProps = {
    display_picks: true,
    season: '2016',
    week: '1'
  };

export default GameList;
