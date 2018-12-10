import React, {Component} from 'react';
import { Tabs, Row, Col, Select } from 'antd';
import { withRouter } from 'react-router-dom';

import GameList from './GameList';

import './Home.css';

const TabPane = Tabs.TabPane;        
const Option = Select.Option;
        
class Home extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleShowPicks = this.handleShowPicks.bind(this);
    this.state = {
      showPicks: false
    };
  }

  componentDidMount() {
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
  }

  handleShowPicks(showPicks) {
    console.log("Updating show picks: " + showPicks);
    this.setState({showPicks: showPicks});
  }

  handleChange(value) {
    this.props.history.push(`/games/${value}/${this.props.week}`);
    window.scrollTo(0, 0);
  }

  render() {
    const weeks = Array(17).fill().map((e,i)=>i+1);
    const startingSeason = 2015;
    const seasons = Array(this.props.currentSeason - startingSeason + 1)
                    .fill().map((e,i)=>i+startingSeason);
    return (
      <div className="Home">
        <Row>
          <Col>
            <Tabs
              ref={element => this.divRef = element}
              defaultActiveKey={this.props.currentWeek}
              tabPosition="top"
              onChange={key => {
                this.props.history.push(`/games/${this.props.season}/${key}`);
              }}
            >
              {weeks.map((week, i) =>
                <TabPane tab={"Week " + week} key={week}>
                  <GameList
                    season={this.props.season}
                    week={week}
                    showPicks={this.state.showPicks}
                    allowScores={this.props.currentWeek === week.toString() && this.props.currentSeason === this.props.season}
                    handleShowPicks = {this.handleShowPicks} 
                    signedInUser = {this.props.signedInUser} />
                </TabPane>
              )}
            </Tabs>
          </Col>
        </Row>
        <Row type="flex" justify="center">
          <Col>
            <br/>
            Select a different season to view past results: &nbsp;
            <Select
              showSearch
              defaultValue={ this.props.season }
              optionFilterProp="children"
              onChange={this.handleChange}
              filterOption={(input, option) => option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
            >
              { seasons.map((season, i) => <Option value={season.toString()} key={season}>{season}</Option> )}
            </Select>
          </Col>
        </Row>
      </div>
    );
  }
}

export default withRouter(Home);
