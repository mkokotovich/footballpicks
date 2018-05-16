import React from 'react';

import './Pick.css';

function Pick(props) {
  return (
    <span className="Pick">
      {props.pick.user_name} &nbsp;
    </span>
  );
}

export default Pick;
