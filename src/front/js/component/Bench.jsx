import React from "react"
import { Player } from "./Player.jsx";

export const Bench = () => {
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
    }
    ]
    const coachData={
        uid: 1,
        name: "Pedro",
        photo: "https://media.api-sports.io/football/players/730.png",
        points: 15
    }
    
    return (
        <div className="d-flex flex-column">
            <Player {...coachData}/>
                    <div className="d-flex flex-wrap">
                        {data.map(player => (<Player {...player} isInBench={true}/>
                        ))}
                    </div>
        </div>
    )
}