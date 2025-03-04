import React from "react";
import { Table } from "../component/Table/Table.jsx";
import { TableStandings } from "../component/Table/TableStandings.jsx";
import { LegendStandings } from "../component/Table/LegendsStandings.jsx";

export const Standings = () => {

    const headers = [
        { label: "#", style: { width: '20px' } }, 
        { label: "Club", style: { width: '200px' } }, 
        { label: "PJ", style: { width: 'auto' } }, 
        { label: "V", style: { width: 'auto' } }, 
        { label: "E", style: { width: 'auto' } }, 
        { label: "D", style: { width: 'auto' } }, 
        { label: "GF", style: { width: 'auto' } }, 
        { label: "GC", style: { width: 'auto' } }, 
        { label: "DF", style: { width: 'auto' } }, 
        { label: "Puntos", style: { width: 'auto' } }, 
        { label: "Últimos 5", style: { width: 'auto' } }, 
    ]

    const data = [
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/529.png', 
                name: 'Barcelona',
            },
            gamesTotal: 22,
            gamesWon: 19,
            gamesTied: 1,
            gamesLost: 2,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 58,
            form: "VVDEV"
        },
        {
            team: {
                logo: 'https://media.api-sports.io/football/teams/530.png', 
                name: 'Atletico Madrid',
            },
            gamesTotal: 22,
            gamesWon: 18,
            gamesTied: 1,
            gamesLost: 3,
            goalsFor: 33,
            goalsAgainst: 10,
            goalsDiff: 23,
            points: 55,
            form: "EVDVV"
        },
    ]
    return (
        <div className="container-fluid">
            <h1 className="text-center">Resultados</h1>
            <div className="container">
                <Table headers={headers} footer={<LegendStandings />}>
                    <TableStandings data={data} />
                </Table>
            </div>
        </div>
    )
}

