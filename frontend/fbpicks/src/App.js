import React from 'react';
import { Button } from 'antd';

import GameList from './GameList'

const App = () => {
  return (
    <div className="App">
      <Button type="primary">Button</Button>
      <GameList season='2016' week='2'/>
    </div>
  );
};

export default App;
