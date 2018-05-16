import React from 'react';

import Pick from './Pick';
import './PickList.css';

function PickList(props) {
  const picks_for_team = props.picks.reduce((picks_for_team, pick) => {
    if (pick.team_to_win === props.team.id) {
      picks_for_team.push(pick);
    }
    return picks_for_team;
  }, []);
  return (
    <div className="PickList">
      {picks_for_team.map((pick, i) => <Pick pick={pick} key={i} />)}
    </div>
  );
}

export default PickList;
