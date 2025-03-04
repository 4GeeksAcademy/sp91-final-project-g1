import React, { useEffect } from "react"
import { useNavigate } from "react-router-dom";
import { Player } from "./Player.jsx";

export const LineUp = () => {
    const navigate = useNavigate()
    const data = [{
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Midfielder"
    },
    {
        uid: 2,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Forward"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Defender"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Goalkeeper"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Defender"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Defender"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Defender"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Midfielder"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Midfielder"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Forward"
    },
    {
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15,
        position: "Forward"
    },
    ]
    const goalkeepers = data.filter(player => player.position === "Goalkeeper");
    const forwards = data.filter(player => player.position === "Forward");
    const defenders = data.filter(player => player.position === "Defender");
    const midfielders = data.filter(player => player.position === "Midfielder");

    return (
        <div className="text-center d-flex flex-column align-items-center">
            <div className="d-flex gap-2 ">
                {forwards.map(player => (<Player {...player} />
                ))}
            </div>
            <div className="d-flex gap-2 ">
                {midfielders.map(player => (<Player {...player} />
                ))}
            </div>
            <div className="d-flex gap-2 ">
                {defenders.map(player => (<Player {...player} />
                ))}
            </div>
            <div className="d-flex gap-2 ">
                {goalkeepers.length > 0 && (
                    <Player {...goalkeepers[0]} key={goalkeepers[0].uid} />
                )}
            </div>
        </div>)
}