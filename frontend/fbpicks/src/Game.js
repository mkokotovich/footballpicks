import React, { Component } from 'react';

class Game extends Component {

  render() {
    return (
      <div className="Game">
        Week {this.props.game.week}: {this.props.game.away_team} at {this.props.game.home_team}
      </div>
    );
  }
}

export default Game;
