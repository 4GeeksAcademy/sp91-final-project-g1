import React from "react";
import { Table } from "../component/Table/Table.jsx";
import { TableStandings } from "../component/Table/TableStandings.jsx";
import { useProtectedPage } from "../hooks/useProtectedPage.js";

export const MyLeague = () => {
    const user = useProtectedPage();
    const headers = [
        { label: "#", style: { width: '20px' } }, 
        { label: "Club", style: { width: '200px' } }, 
        { label: "GF", style: { width: 'auto' } }, 
        { label: "TA", style: { width: 'auto' } },
        { label: "TR", style: { width: 'auto' } },
        { label: "Puntos", style: { width: 'auto' } }, 
    ]

    const data = [
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Pepito FC'
            },
            goalsFor: 35,
            yellowCards: 25,
            redCards: 3,
            points: 23
        }
    ]

    return (
        <div className="container-fluid">
            <div className="d-flex gap-3 justify-content-center align-items-center">
                <h1 className="text-center">Mi liga</h1>
                <button className="btn btn-outline-primary">Añadir equipo</button>
            </div>
            <div className="container">
                {
                    data.length > 0
                    ?
                    <Table headers={headers}>
                        <TableStandings data={data} />
                    </Table>
                    :
                    <div className="d-flex flex-column align-items-center justify-content-center mt-5 gap-3">
                        <span className="mt-5">No te has unido a una liga</span>
                        <button className="btn btn-primary px-3">Unirse a liga</button>
                    </div>
                }
            </div>
        </div>
    )
}