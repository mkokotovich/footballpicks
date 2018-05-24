import React, {Component} from 'react';
import { Tabs, Row, Col, Select } from 'antd';

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
      season: props.currentSeason,
      showPicks: false
    };
  }

  handleShowPicks(showPicks) {
    console.log("Updating show picks: " + showPicks);
    this.setState({showPicks: showPicks});
  }

  handleChange(value) {
    this.setState({season: value});
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
            >
              {weeks.map((week, i) =>
                <TabPane tab={"Week " + week} key={week}>
                  <GameList
                    season={this.state.season}
                    week={week}
                    showPicks={this.state.showPicks}
                    handleShowPicks = {this.handleShowPicks} 
                    signedInUser = {this.props.signedInUser} />
                </TabPane>)}
            </Tabs>
          </Col>
        </Row>
        <Row type="flex" justify="center">
          <Col>
            <br/>
            Select a different season to view past results: &nbsp;
            <Select
              showSearch
              defaultValue={ this.props.currentSeason }
              optionFilterProp="children"
              onChange={this.handleChange}
              filterOption={(input, option) => option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
            >
              { seasons.map((season, i) => <Option value={season} key={season}>{season}</Option> )}
            </Select>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Home
