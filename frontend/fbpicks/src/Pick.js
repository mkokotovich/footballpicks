import React, { Component } from 'react';
import { Row, Col } from 'antd';

class Pick extends Component {

  render() {
    return (
      <div className="Pick">
        {this.props.pick.user_name}
      </div>
    );
  }
}

export default Pick;
