import React from 'react'

function Square (props) {
    const style = {
        width: 50, 
        height: 40
    }
    return (
        <button className="square" style={ style } onClick={ props.onClick }>
            {props.value}
        </button>
    )
}

export default Square;