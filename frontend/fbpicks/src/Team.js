import React from 'react';
import { Row, Col } from 'antd';

import './Team.css';

function Team(props) {
  const tieString = props.team.ties === 0 ? "" : "-" + props.team.ties;
  const recordString = "(" + props.team.wins + "-" + props.team.loses + tieString + ")";
  const justify = props.home === true ? "start" : "end";
  const logoOrder = props.home === true ? 1 : 2;
  const nameOrder = props.home === true ? 2 : 1;
  const textStyle = {
    textAlign: props.home === true ? "left" : "right",
  };
  return (
    <div className="Team">
      <Row type="flex" justify={justify} style={textStyle}>
        <Col order={nameOrder}>
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
        {/*
        <Col order={logoOrder}>
          <img src="http://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/dal.png&h=30&w=30"/>
        </Col>
        */}
      </Row>
    </div>
  );
}

export default Team;
