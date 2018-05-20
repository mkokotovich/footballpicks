import React from 'react';
import moment from 'moment';

import './GameTime.css'

function GameTime(props) {
  const momentDate = moment(new Date(props.game.game_time))

  return (
    <div className="GameTime">
      {momentDate.format('dddd')}
      <br/>
      {momentDate.format('MMM')} {momentDate.format('Do')}, {momentDate.format('YYYY')}
      <br/>
      {momentDate.format('LT')}
    </div>
  );
}

export default GameTime;
