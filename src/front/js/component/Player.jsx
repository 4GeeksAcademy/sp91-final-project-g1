import React from "react"
import playerBg from "../../img/playerBg.png";
import PropTypes from "prop-types";


export const Player = (props) => {
    const size = props.isInBench ? 150 : 175
    return ( 
        <div class={`card text-white border-0`} style={{ width: `${size}px`, height: `${size}px` }}>
            <img class="card-img" src={playerBg} alt="Card image" />
            <div class={`card-img-overlay d-flex flex-column justify-content-center align-items-center ${props.isInBench && "p-0"}`}>
                <img src={props.photo} className="card-text " height={size * 0.4} width={size * 0.4} />
                <p className="card-title m-0">{props.name}</p>
                <p className={`card-text ${!props.isInBench && "fs-5"} m-0`}>{props.points}</p>
            </div>
        </div>
    )
}
Player.propTypes = {
    player: PropTypes.object,
    isInBench: PropTypes.bool,
}
Player.defaultProps = {
    player: {},
    isInBench: false,
}
