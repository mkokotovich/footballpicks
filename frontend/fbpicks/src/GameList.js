import React, { Component } from 'react';
import axios from 'axios';

import './GameList.css';

import Game from './Game';

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
        {this.state.games.map((game, i) => <Game game={game} key={i} />)}
      </div>
    );
  }

  componentDidMount() {
    axios.get('/api/v1/games/', {
        params: {
          season: this.props.season,
          week: this.props.week,
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
}

GameList.defaultProps = {
    season: '2016',
    week: '1'
  };

export default GameList;