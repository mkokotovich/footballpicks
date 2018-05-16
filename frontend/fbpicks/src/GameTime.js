import React from 'react';

function GameTime(props) {
  const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sept", "Oct", "Nov", "Dec" ];

  const date = new Date(props.game.game_time);
  const month = monthNames[date.getMonth()]

  return (
    <div className="GameTime">
      <br/>
      at
      <br/>
      {month} {date.getDate()}, {date.toLocaleTimeString()}
    </div>
  );
}

export default GameTime;
