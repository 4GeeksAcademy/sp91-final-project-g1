import React from "react"
import { Player } from "./Player.jsx";

export const LineUp = (props) => {
    const [defendersCount, midFieldersCount, forwardsCount] = props.data.formation.split('-')
    const goalkeeper = props.data.players.find(player => player.position === 1);

    const generatePlayers = (count, offset = 0) => {
        const players = []

        for (let i = 1; i <= count; i++) {
            console.log(i + 1 + offset);

            const player = props.data.players.find(player => player.position === i + 1 + offset)
            players.push(<Player {...player} key={player?.uid} />)
        }

        return players;
    }

    return (
        <div className="text-center d-flex flex-column align-items-center">
            <div className="d-flex gap-2 ">
                {generatePlayers(parseInt(forwardsCount), parseInt(defendersCount) + parseInt(midFieldersCount))}
            </div>
            <div className="d-flex gap-2 ">
                {generatePlayers(parseInt(midFieldersCount), parseInt(defendersCount))}
            </div>
            <div className="d-flex gap-2 ">
                {generatePlayers(parseInt(defendersCount))}
            </div>
            <div className="d-flex gap-2 ">
                <Player {...goalkeeper} key={goalkeeper?.uid} />
            </div>
        </div>)
}