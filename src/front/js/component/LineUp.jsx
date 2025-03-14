import React from "react"
import { Player } from "./Player.jsx";

export const LineUp = (props) => {
    const [defendersCount, midFieldersCount, forwardsCount] = props.data.formation.split('-')
    const goalkeeper = props.data.players.find(player => player.position === 'Goalkeeper');

    const generatePlayers = (count, position) => {
        const players = []

        const playersOfPosition = props.data.players.filter(player => player.position === position)
        
        const existingPlayers = []
        for (const player of playersOfPosition) {
            const playerAlreadyAdded = existingPlayers.find((playerAlready) => playerAlready.player_id === player.player_id)
            
            if (!playerAlreadyAdded) {
                existingPlayers.push(player)
                players.push(<Player player={player} key={player?.player_id} />)
            }
        }
        if(players.length < count) {
            for (let i = players.length; i < count; i++) {
                players.push(<Player />)
            }
        }

        return players;
    }

    return (
        <div className="text-center d-flex flex-column align-items-center">
            <div className="d-flex gap-2 ">
                {generatePlayers(parseInt(forwardsCount), 'Attacker')}
            </div>
            <div className="d-flex gap-2 ">
                {generatePlayers(parseInt(midFieldersCount), 'Midfielder')}
            </div>
            <div className="d-flex gap-2 ">
                {generatePlayers(parseInt(defendersCount), 'Defender')}
            </div>
            <div className="d-flex gap-2 ">
                <Player player={goalkeeper} key={goalkeeper?.uid} />
            </div>
        </div>)
}