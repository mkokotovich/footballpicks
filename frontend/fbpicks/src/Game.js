import React, { Component } from 'react';

class Game extends Component {

  render() {
    return (
      <div className="Game">
        Week {this.props.game.week}: {this.props.game.away_team.team_name} at {this.props.game.home_team.team_name}
      </div>
    );
  }
}

export default Game;
