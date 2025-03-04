import React from "react"

export const TeamData = () => {
    const data = {
        logo: 'https://media.api-sports.io/football/teams/529.png',
        name: 'Pepito FC',
        points: 15
    }
    return(
        <div className="align-items-center d-flex flex-column justify-content-center">
            <img src={data.logo}  width={100} height={100}/>
            <p class="card-text fs-5 m-0">{data.name}: {data.points} puntos</p>
        </div>
    )
}