import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import $ from 'jquery';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn,} from 'material-ui/Table';

class GameStats extends Component {
    constructor(props) {
        super(props);

        this.getScores();

        this.state = {
            zero: 0,zerouser:'',
            one:0,oneuser:'',
            two:  0, twouser:'',
            three:  0, threeuser:'',
            four: 0, fouruser:'',
            five:  0, fiveuser:'',
            six:  0, sixuser:'',
            seven:  0, sevenuser:'',
            eight: 0, eightuser:'',
            nine: 0, nineuser:'',
        }
    }

    render() {
        return (
            <div align="center">
            <MuiThemeProvider>
            <div>
            <p>These scores were retrieved from pre-loaded data stored in the db</p>
            <Table style={{ width: 200}}>
                    <TableHeader displaySelectAll={false}>
                      <TableRow>
                        <TableHeaderColumn>Username</TableHeaderColumn>
                        <TableHeaderColumn>Score</TableHeaderColumn>
                      </TableRow>
                    </TableHeader>
                    <TableBody displayRowCheckbox={false} >
                      <TableRow>
                        <TableRowColumn>{this.state.zerouser}</TableRowColumn>
                        <TableRowColumn>{this.state.zero}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.oneuser}</TableRowColumn>
                        <TableRowColumn>{this.state.one}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.twouser}</TableRowColumn>
                        <TableRowColumn>{this.state.two}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.threeuser}</TableRowColumn>
                        <TableRowColumn>{this.state.three}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.fouruser}</TableRowColumn>
                        <TableRowColumn>{this.state.four}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.fiveuser}</TableRowColumn>
                        <TableRowColumn>{this.state.five}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.sixuser}</TableRowColumn>
                        <TableRowColumn>{this.state.six}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.sevenuser}</TableRowColumn>
                        <TableRowColumn>{this.state.seven}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.eightuser}</TableRowColumn>
                        <TableRowColumn>{this.state.eight}</TableRowColumn>
                      </TableRow>
                      <TableRow>
                        <TableRowColumn>{this.state.nineuser}</TableRowColumn>
                        <TableRowColumn>{this.state.nine}</TableRowColumn>
                      </TableRow>
                    </TableBody>
                  </Table>
                  </div>
              </MuiThemeProvider>
            </div>
        )};


        getScores() {
            $.ajax({ 
                url: "/api/leaderBoard/topTen/",
                headers: {'Authorization': "Bearer " + this.props.userToken},
                method: "GET",
                contentType: "application/json; charset=UTF-8",
            }).done((data , text_status, jqXHR)=>{
                console.log(text_status);
                console.log(jqXHR.status);
                
                this.setState({
                    zero: data[1][1], zerouser:data[1][0],
                    one: data[2][1], oneuser:data[2][0],
                    two: data[3][1], twouser:data[3][0],
                    three: data[4][1], threeuser:data[4][0],
                    four: data[5][1], fouruser:data[5][0],
                    five: data[6][1], fiveuser:data[6][0],
                    six: data[7][1], sixuser:data[7][0],
                    seven:data[8][1], sevenuser:data[8][0],
                    eight: data[9][1], eightuser:data[9][0],
                    nine: data[10][1], nineuser:data[10][0],
                });
        
            }).fail((err)=>{
                alert(JSON.stringify(err.responseJSON));
                console.log(err.status);
                console.log(JSON.stringify(err.responseJSON));
            });
          };
      

}

export default GameStats;