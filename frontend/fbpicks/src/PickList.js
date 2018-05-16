import React, { Component } from 'react';

import Pick from './Pick';

class PickList extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const picks_for_team = this.props.picks.reduce((picks_for_team, pick) => {
      if (pick.team_to_win === this.props.team.id) {
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
}

export default PickList;
