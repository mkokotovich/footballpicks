import React, { Component } from 'react';

class Team extends Component {

  render() {
    return (
      <div className="Team">
        {this.props.team.team_name}
      </div>
    );
  }
}

export default Team;
