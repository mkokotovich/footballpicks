import React, { Component } from 'react';
import { Row, Col } from 'antd';

import Team from './Team';
import GameTime from './GameTime';

class Game extends Component {

  render() {
    return (
      <div className="Game">
        <Row type="flex" justify="center" align="top">
          <Col span={8}> <Team team={this.props.game.away_team} /> </Col>
          <Col span={4}> <GameTime game={this.props.game} /> </Col>
          <Col span={8}> <Team team={this.props.game.home_team} /> </Col>
        </Row>
      </div>
    );
  }
}

export default Game;
