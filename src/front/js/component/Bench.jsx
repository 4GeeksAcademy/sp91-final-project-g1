import React from "react"
import { Player } from "./Player.jsx";

export const Bench = (props) => {

    const coach = props.data.players.find(player => player.position === "Coach")

    const generateBench = () => {
        const players = []

        const playersInBench = props.data.players.filter(player => player.isInBench)
        for (const player of playersInBench) {
            players.push(<Player player={player} key={player.uid} />)
        }

        if (players.length < 5) {
            for (let i = players.length; i < 5; i++) {
                players.push(<Player />)  
            }
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
