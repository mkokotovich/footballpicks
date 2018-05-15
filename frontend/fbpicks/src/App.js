import React from 'react';

import GameList from './GameList'
import SignIn from './SignIn'

const App = () => {
  return (
    <div className="App">
      <SignIn/>
      <GameList season='2016' week='2'/>
    </div>
  );
};

export default App;
