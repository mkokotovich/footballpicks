import React from 'react';
import { Row, Col } from 'antd';

import './Team.css';

function Team(props) {
  const tieString = props.team.ties === 0 ? "" : "-" + props.team.ties;
  const recordString = "(" + props.team.wins + "-" + props.team.loses + tieString + ")";
  return (
    <div className="Team">
      <Row type="flex" justify="center" align="middle">
        <Col xs="24" sm="12">
          <span className="TeamName">
            {props.team.team_name} 
          </span> 
        </Col>
        <Col xs="24" sm="12">
          <span className="TeamRecord">
            {recordString}
          </span>
        </Col>
      </Row>
    </div>
  );
}

export default Team;
