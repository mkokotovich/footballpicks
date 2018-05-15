import React from 'react';
import { Row, Col } from 'antd';

import GameList from './GameList'
import SignIn from './SignIn'

const App = () => {
  return (
    <div className="App">
      <Row type="flex" justify="space-between">
        <Col><h2>Welcome to Football Picks</h2></Col>
        <Col><SignIn/></Col>
      </Row>
      <GameList season='2016' week='2'/>
    </div>
  );
};

export default App;
