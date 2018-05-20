import React from 'react';
import { Row, Col } from 'antd';

import './Team.css';

function Team(props) {
  const tieString = props.team.ties === 0 ? "" : "-" + props.team.ties;
  const recordString = "(" + props.team.wins + "-" + props.team.loses + tieString + ")";
  const justify = props.home === true ? "start" : "end";
  const textStyle = {
    textAlign: props.home === true ? "left" : "right",
  };
  return (
    <div className="Team">
      <Row type="flex" justify={justify} style={textStyle}>
        <Col>
          <Row type="flex" justify={justify}>
            <Col>
              <span className="TeamName">
                {props.team.team_name} 
              </span> 
            </Col>
          </Row>
          <Row type="flex" justify={justify}>
            <Col>
              <span className="TeamRecord">
                {recordString}
              </span>
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  );
}

export default Team;
