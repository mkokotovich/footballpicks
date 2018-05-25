import React, { Component } from 'react';
import { Row, Col } from 'antd';

import './Team.css';

class Team extends Component {
  constructor(props) {
    super(props);
    this.state = {
      checked: props.checked
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(event) {
    this.props.handleSetPick(this.props.gameID, this.props.team.id);
    this.setState({checked: event.target.checked});
  }

  render() {
    const tieString = this.props.team.ties === 0 ? "" : "-" + this.props.team.ties;
    const recordString = "(" + this.props.team.wins + "-" + this.props.team.loses + tieString + ")";
    const justify = this.props.home === true ? "start" : "end";
    const textStyle = {
      textAlign: this.props.home === true ? "left" : "right",
    };
    const checkboxStyle = {
      marginLeft: this.props.home ? "0px" : "5px",
      marginRight: this.props.home ? "5px" : "0px",
      verticalAlign: "4px",
    }
    const labelID = this.props.home ? "home" + this.props.gameID : "away" + this.props.gameID;
    const smPush = this.props.home ? 2 : 0;
    const smPull = this.props.home ? 22 : 0;
    const mdPush = this.props.home ? 1 : 0;
    const mdPull = this.props.home ? 23 : 0;
    const checkbox = (
      <input
        type="checkbox"
        name={labelID}
        style={checkboxStyle}
        id={labelID}
        checked={this.state.checked}
        onChange={this.handleClick} />
    );
    const teamNameOnly = (
      <span className="TeamName">
        {this.props.team.team_name} 
      </span> 
    );
    const teamName = this.props.submitting ? (
      <Row type="flex" justify={justify} >
        <form style={{width: "100%"}}>
          <label>
            <Col xs={24} sm={{ span: 22, push: smPush}} md={{ span: 23, push: mdPush}}>
              { teamNameOnly }
            </Col>
            <Col xs={24} sm={{span: 2, pull: smPull}} md={{ span: 1, pull: mdPull}}>
              { checkbox }
            </Col>
          </label>
        </form>
      </Row>
    ) : (
      <Row type="flex" justify={justify}>
        <Col>
        <span className="TeamName">
          {this.props.team.team_name} 
        </span> 
        </Col>
      </Row>
    );

    return (
      <Row type="flex" justify={justify} style={textStyle}>
        <Col span={24}>
          { teamName }
          <Row>
            <Col>
              <span className="TeamRecord">
                {recordString}
              </span>
            </Col>
          </Row>
        </Col>
      </Row>
    );
  }

  /*
   * TODO
  https://reactjs.org/docs/forms.html#handling-multiple-inputs
  */
  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps.checked !== this.props.checked) {
      this.setState({checked: this.props.checked});
    }
  }
}

export default Team;
