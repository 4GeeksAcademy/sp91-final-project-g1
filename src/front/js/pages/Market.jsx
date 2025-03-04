import React, { useContext, useEffect, useState } from "react";
import { Table } from "../component/Table/Table.jsx";
import { TableMarket } from "../component/Table/TableMarket.jsx";
import { Context } from "../store/appContext.js";

export const Market = () => {

    const { actions } = useContext(Context)
    const [data, setData] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    const getPlayers = async() => {
        const playerData = await actions.api.get('players-market', 'limit=15')
        console.log(playerData)
        setData(playerData)
        setIsLoading(false)
    }

    useEffect(() => {
        getPlayers()
    }, [])
    /*
    const data = [
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Barcelona'
            },
            photo: "https://media.api-sports.io/football/players/18742.png",
            position: "Goalkeeper",
            name: "T. Courtois",
            fantasyTeam: null,
            points: 0,
            marketValue: 187000,
            clauseValue: null
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Barcelona'
            },
            photo: "https://media.api-sports.io/football/players/731.png",
            position: "Defender",
            name: "T. Courtos",
            fantasyTeam: {
                logo: 'https://media.api-sports.io/football/teams/33.png',
                name: 'Equipo xd'
            },
            points: 15,
            marketValue: 33000000,
            clauseValue: 123456789
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Barcelona'
            },
            photo: "https://media.api-sports.io/football/players/10009.png",
            position: "Midfielder",
            name: "T. Courtois",
            fantasyTeam: null,
            points: 0,
            marketValue: 187000,
            clauseValue: null
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Barcelona'
            },
            photo: "https://media.api-sports.io/football/players/731.png",
            position: "Forward",
            name: "T. Courtos",
            fantasyTeam: {
                logo: 'https://media.api-sports.io/football/teams/33.png',
                name: 'Equipo xd'
            },
            points: 15,
            marketValue: 33000000,
            clauseValue: 123456789
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Barcelona'
            },
            photo: "https://media.api-sports.io/football/players/10009.png",
            position: "Goalkeeper",
            name: "T. Courtois",
            fantasyTeam: null,
            points: 0,
            marketValue: 187000,
            clauseValue: null
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Barcelona'
            },
            photo: "https://media.api-sports.io/football/players/731.png",
            position: "Defender",
            name: "T. Courtos",
            fantasyTeam: {
                logo: 'https://media.api-sports.io/football/teams/33.png',
                name: 'Equipo xd'
            },
            points: 15,
            marketValue: 33000000,
            clauseValue: 123456789
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Barcelona'
            },
            photo: "https://media.api-sports.io/football/players/10009.png",
            position: "Midfielder",
            name: "T. Courtois",
            fantasyTeam: null,
            points: 0,
            marketValue: 187000,
            clauseValue: null
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png',
                name: 'Barcelona'
            },
            photo: "https://media.api-sports.io/football/players/731.png",
            position: "Forward",
            name: "T. Courtos",
            fantasyTeam: {
                logo: 'https://media.api-sports.io/football/teams/33.png',
                name: 'Equipo xd'
            },
            points: 15,
            marketValue: 33000000,
            clauseValue: 123456789
        }
    ]
    */

    return (
        <div className="container-fluid">
            <h1 className="text-center">Mercado de fichajes</h1>
            <div className="container col-9 col-lg-6 col-xl-4">
                {!isLoading && 
                <Table headers={[]}>
                    <TableMarket data={data} />
                </Table>}
            </div>
        </div>
    )
}
