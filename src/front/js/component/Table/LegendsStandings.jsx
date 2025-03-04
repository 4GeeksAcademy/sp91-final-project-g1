import React from "react"

export const LegendStandings = () => {

    return (
        <tr>
            <td colSpan={6}>
                <p>Ascenso/Descenso</p>
                <div>
                    <i className="fa-solid fa-square text-info pe-1"></i> Fase de grupos de Champions League
                </div>
                <div>
                    <i className="fa-solid fa-square text-warning pe-1"></i> Fase de grupos de Europa League
                </div>
                <div>
                <i className="fa-solid fa-square text-success pe-1"></i>Clasificados de Conference League
                </div>
                <div>
                    <i className="fa-solid fa-square text-danger pe-1"></i> Descenso
                </div>
            </td>
            <td colSpan={5} valign="top">
                <p>Últimos 5 partidos</p>
                <div>
                    <i className="fa-solid fa-circle-check text-success pe-1"></i> Victoria
                </div>
                <div>
                    <i className="fa-solid fa-circle-xmark text-danger pe-1"></i> Derrota
                </div>
                <div>
                    <i className="fa-solid fa-circle-minus text-secondary pe-1"></i> Empate
                </div>
            </td>
        </tr>
    )
}