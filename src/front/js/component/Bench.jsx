import React from "react"
import { Player } from "./Player.jsx";

export const Bench = () => {
    const data = []
    
    return (
        <div className="d-flex flex-column">
            <Player />
                    <div className="d-flex flex-wrap">
                        {data.map(player => (<Player {...player} isInBench={true}/>
                        ))}
                    </div>
        </div>
    )
}