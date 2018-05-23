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
    const nameAndCheck = this.props.home ? (
      <label>
        { checkbox }
        { teamNameOnly }
      </label>
    ) : (
      <label>
        { teamNameOnly }
        { checkbox }
      </label>
    );
    const teamName = this.props.submitting ? (
      <form>
        { nameAndCheck }
      </form>
    ) : (
      <span className="TeamName">
        {this.props.team.team_name} 
      </span> 
    );

    return (
      <Row type="flex" justify={justify} style={textStyle}>
        <Col>
          <Row type="flex" justify={justify}>
            <Col>
              { teamName }
            </Col>
          </Row>
          <Row type="flex" justify={justify}>
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
