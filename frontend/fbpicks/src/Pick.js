import React from 'react';

import './Pick.css';

function Pick(props) {
  return (
    <span className="Pick">
      { props.home !== true && <span> &nbsp;</span> }
      { props.pick.user.first_name }
      { props.home === true && <span> &nbsp;</span> }
    </span>
  );
}

export default Pick;
