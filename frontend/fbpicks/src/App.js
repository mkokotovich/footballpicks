import React from 'react';
import { Row, Col } from 'antd';

import GameList from './GameList';
import SignIn from './SignIn';

import './App.css';

const App = () => {
  return (
    <div className="App">
      <Row type="flex" justify="space-between" className="navbar" align="middle">
        <Col className="Logo">Football Picks</Col>
        <Col><SignIn/></Col>
      </Row>
      <GameList season='2016' week='2'/>
    </div>
  );
};

export default App;
