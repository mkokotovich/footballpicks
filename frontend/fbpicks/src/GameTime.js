import React, { Component } from 'react';

class GameTime extends Component {

  render() {
    const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
  "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];

    const date = new Date(this.props.game.game_time);
    const month = monthNames[date.getMonth()]

    return (
      <div className="GameTime">
        at
        <br/>
        {month} {date.getDate()}, {date.toLocaleTimeString()}
      </div>
    );
  }
}

export default GameTime;
