import React, { Component } from 'react';
import axios from 'axios';
import { Select, Table, Radio, Modal, Spin, Col, Row } from 'antd';
import { withRouter } from 'react-router-dom';

import './Records.css';

const Option = Select.Option;

class Records extends Component {
  constructor(props) {
    super(props);
    this.state = {
      season: this.props.currentSeason,
      week: this.props.currentWeek,
      records: [],
      loading: false,
      radioValue: "week",
    };
  }

  componentDidMount() {
      this.retrieveRecords();
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps.season !== this.props.season || prevProps.week !== this.props.week) {
      this.retrieveRecords();
    }
    if (prevState.season !== this.state.season || prevState.week !== this.state.week) {
      this.retrieveRecords();
    }
  }

  retrieveRecords() {
    this.setState({loading: true});
    var params = {};
    if (this.state.season) {
      params["season"] = this.state.season;
    }
    if (this.state.week) {
      params["week"] = this.state.week;
    }
    axios.get('/api/v1/records/', {
      params: params
      })
      .then((response) => {
        const records = response.data.results;
        this.setState({
          loading: false,
          records: records
        });
      })
      .catch((error) => {
        console.log(error);
        this.setState({loading: false});
        Modal.error({
          title: "Unable to load records",
          content: "Unable to load records. Please try again.\n\n" + error,
          maskClosable: true,
        })
      });
  }

  onChange = (e) => {
    var newState = {};
    if (e.target.value === "week") {
      newState = {
        week: this.state.week ? this.state.week : this.props.currentWeek,
        season: this.state.season ? this.state.season : this.props.currentSeason,
        radioValue: e.target.value,
      }
    }
    if (e.target.value === "season") {
      newState = {
        week: undefined,
        season: this.state.season ? this.state.season : this.props.currentSeason,
        radioValue: e.target.value,
      }
    }
    if (e.target.value === "alltime") {
      newState = {
        week: undefined,
        season: undefined,
        radioValue: e.target.value,
      }
    }

    this.setState(newState, () => this.retrieveRecords());
  }


  columns = [{
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    }, {
      title: 'Win',
      dataIndex: 'win',
      key: 'win',
    }, {
      title: 'Loss',
      dataIndex: 'loss',
      key: 'loss',
    }, {
      title: 'Percentage',
      key: 'percentage',
      dataIndex: 'percentage',
      render: percentage => (
        (parseFloat(percentage) * 100).toFixed(1) + '%'
      ),
    }
  ];

  render() {
    const weeks = Array(17).fill().map((e,i)=>i+1);
    const startingSeason = 2015;
    const seasons = Array(this.props.currentSeason - startingSeason + 1)
                    .fill().map((e,i)=>i+startingSeason);

    const seasonSelector = (
      <Select
        showSearch
        defaultValue={ this.props.currentSeason }
        optionFilterProp="children"
        filterOption={(input, option) => option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
        onChange={value => {
          this.setState({season: value});
        }}
      >
        { seasons.map((season, i) => <Option value={season.toString()} key={season}>{season}</Option> )}
      </Select>
    );

    const weekSelector = (
      <Select
        showSearch
        defaultValue={ this.props.currentWeek }
        optionFilterProp="children"
        filterOption={(input, option) => option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
        onChange={value => {
          this.setState({week: value});
        }}
      >
        { weeks.map((week, i) => <Option value={week.toString()} key={week}>{week}</Option> )}
      </Select>
    );
    return (
      <div className="Records">
        <Row type="flex" gutter={20} align="middle">
        <Col>
          <Radio.Group onChange={this.onChange} value={this.state.radioValue} buttonStyle="solid">
            <Radio.Button value="week">Week</Radio.Button>
            <Radio.Button value="season">Season</Radio.Button>
            <Radio.Button value="alltime">All Time</Radio.Button>
          </Radio.Group>
        </Col>
        
        { (this.state.radioValue === "season" || this.state.radioValue === "week") && (
          <Col>
            <div>
              Select Season: { seasonSelector }
            </div>
          </Col>
        )}
        { this.state.radioValue === "week" && (
          <Col>
            <div>
              Select Week: { weekSelector }
            </div>
          </Col>
        )}
        </Row>

        <br/> <br/>

        <Table columns={this.columns} dataSource={this.state.records} />

        <Row type="flex" justify="center">
          <Col>
            { this.state.loading && <Spin size="large" /> }
          </Col>
        </Row>

      </div>
    );
  }

}

export default withRouter(Records);
