import React from 'react'
import Board from './components/Board'

export default class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            history: [{
                squares: Array(9).fill(null),
            }],
            stepNumber: 0,
            xIsNext: true,
        };
    }

    jumpTo(step) {
        this.setState({
            stepNumber: step,
            xIsNext: (step % 2) === 0,
        });
    }
    
    handleClick(i) {
        //const history = this.state.history;
        const history = this.state.history.slice(0, this.state.stepNumber + 1);
        const current = history[history.length - 1];
        const sq = current.squares.slice();

        if (calculateWinner(sq) || sq[i]) {
            return false;
        }

        sq[i] = this.state.xIsNext ? 'X' : 'O';
        
        this.setState({
            history : history.concat(
                [{
                    squares: sq,
                }]
            ),
            stepNumber: history.length,
            xIsNext: !this.state.xIsNext
        });
    }

    moves () {
        const history = this.state.history;
        return history.map((step, move) => {
            const desc = move ? 'Go to move #' + move : 'Go to game start';
            return (
                <li key={move}>
                    <button onClick={ () => this.jumpTo(move) }>{desc}</button>
                </li>
            );
        });
    }

    render() {
        const history = this.state.history;
        const current = history[this.state.stepNumber];
        const winner = calculateWinner(current.squares);

        let status;
        if (winner) {
            status = 'Winner: ' + winner;
        } else {
            status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
        }

        return (
            <div className="game">
                <div className="game-board">
                    <Board 
                        squares={ current.squares }
                        onClick={ (i) => this.handleClick(i) }
                    />
                </div>
                <div className="game-info">
                    <div className="status">{status}</div>
                    <ol>{ this.moves() }</ol>
                </div>
            </div>
        );
    }
}

function calculateWinner(squares) {
    const lines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ];
    for (let i = 0; i < lines.length; i++) {
      const [a, b, c] = lines[i];
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return squares[a];
      }
    }
    return null;
}