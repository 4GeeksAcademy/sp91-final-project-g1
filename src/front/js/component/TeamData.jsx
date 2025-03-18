import React from "react"
import teamPlaceholder from '../../img/team-placeholder.png'

export const TeamData = (props) => {
    
    return (
        <div className="align-items-center d-flex flex-column justify-content-center">
            <img src={props.team.logo || teamPlaceholder} width={100} height={100} />
            <p className="card-text fs-5 m-0">{props.team.name}: {props.team.points} puntos</p>
        </div>
    )
}

TeamData.defaultProps = {
    team: {
        name: 'Mi equipo',
        logo: '',
        points: 0
    }
}