import React from "react"
import { Player } from "./Player.jsx";

export const Bench = (props) => {

    const coach = props.data.players.find(player => player.position === 0)

    const generateBench = () => {
        const players = []

        for (let i = 1; i <= 5; i++) {
            const player = props.data.players.find(player => player.position === i + 11)
            players.push(<Player player={player} key={player?.uid} />)
        }

        return players;
    }

    return (
        <div className="d-flex flex-column">
            <Player player={coach} />
            <div className="d-flex flex-wrap">
                {generateBench()}
            </div>
        </div>
    )
}