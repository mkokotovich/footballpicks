import React from 'react';
import { Row, Col } from 'antd';

import Pick from './Pick';
import './PickList.css';

function PickList(props) {
  const picks_for_team = props.picks.reduce((picks_for_team, pick) => {
    if (pick.team_to_win === props.team.id) {
      picks_for_team.push(pick);
    }
    return picks_for_team;
  }, []);

  const justify = props.home === true ? "start" : "end";
  const textStyle = {
    textAlign: props.home === true ? "left" : "right",
  };

  return (
    <Row type="flex" justify={justify} style={textStyle} >
      <Col>
        { props.home !== true && <span> &nbsp; </span> }
        {
          props.display &&
          picks_for_team.map((pick, i) => <Pick pick={pick} key={i} home={props.home}/>)
        }
        { props.home === true && <span> &nbsp; </span> }
      </Col>
    </Row>
  );
}

export default PickList;
