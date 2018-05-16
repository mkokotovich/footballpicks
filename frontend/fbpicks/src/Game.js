import React from 'react';
import { Row, Col } from 'antd';

import Team from './Team';
import GameTime from './GameTime';
import PickList from './PickList';

import './Game.css'

function Game(props) {
  return (
    <div className="Game">
      <Row type="flex" justify="center" align="top">
        <Col span={10}>
          <Team team={props.game.away_team} />
          { props.display_picks && 
            <PickList team={props.game.away_team}
                      picks={props.game.picks} />
          }
        </Col>
        <Col span={4}>
          <GameTime game={props.game} />
        </Col>
        <Col span={10}>
          <Team team={props.game.home_team} />
          { props.display_picks && 
            <PickList team={props.game.home_team}
                      picks={props.game.picks} />
          }
        </Col>
      </Row>
      <br/>
    </div>
  );
}

export default Game;
