import React from 'react';

import './Team.css';

function Team(props) {
  const tieString = props.team.ties === 0 ? "" : "-" + props.team.ties;
  const recordString = "(" + props.team.wins + "-" + props.team.loses + tieString + ")";
  return (
    <div className="Team">
      <div className="TeamName">
        {props.team.team_name}
      </div>
      <div className="TeamRecord">
        {recordString}
      </div>
    </div>
  );
}

export default Team;
