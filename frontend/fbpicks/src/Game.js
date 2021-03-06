import React from 'react';
import { Row, Col } from 'antd';

import Team from './Team';
import GameTime from './GameTime';
import PickList from './PickList';

import './Game.css'

function Game(props) {
  const scoresText = props.game.score && (
    Number(props.game.score.away_score) > Number(props.game.score.home_score) ? (
    <span><b>{props.game.score.away_score}</b> - {props.game.score.home_score}</span>
  ) : Number(props.game.score.away_score) < Number(props.game.score.home_score) ? (
    <span>{props.game.score.away_score} - <b>{props.game.score.home_score}</b></span>
  ) : (
    <span>{props.game.score.away_score} - {props.game.score.home_score}</span>
  ));
  const scoreRow = props.game.score && (
    <Row type="flex" justify="center" align="top" gutter={10}>
      <Col>
        <div className="Scores">
          {scoresText}
        </div>
        <div className="ScoreTime">
          {props.game.score.time}
        </div>
      </Col>
    </Row>
  );
  return (
    <div className="Game">
      <Row type="flex" justify="center" align="top" gutter={10}>
        <Col xs={10}>
          <Team
            team={props.game.away_team}
            home={false}
            submitting={props.submitting}
            gameID={props.gameID}
            handleSetPick={props.handleSetPick}
            checked={props.selectedTeam === props.game.away_team.id}
          />
          <PickList team={props.game.away_team}
                    picks={props.game.picks}
                    home={false} 
                    display={props.display_picks} />
        </Col>
        <Col xs={4}>
          <GameTime game={props.game} />
        </Col>
        <Col xs={10}>
          <Team
            team={props.game.home_team}
            home={true}
            submitting={props.submitting}
            gameID={props.gameID}
            handleSetPick={props.handleSetPick}
            checked={props.selectedTeam === props.game.home_team.id}
          />
          <PickList team={props.game.home_team}
                    picks={props.game.picks} 
                    home={true}
                    display={props.display_picks} />
        </Col>
      </Row>
      { props.showScores &&
        scoreRow
      }
      <br/>
    </div>
  );
}

export default Game;
