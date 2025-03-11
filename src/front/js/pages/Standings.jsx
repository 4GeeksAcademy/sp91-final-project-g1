import React, { useContext, useEffect, useState } from "react";
import { Table } from "../component/Table/Table.jsx";
import { TableStandings } from "../component/Table/TableStandings.jsx";
import { LegendStandings } from "../component/Table/LegendsStandings.jsx";
import { Context } from "../store/appContext.js";

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
        { label: "Pts", style: { width: 'auto' } }, 
        { label: "Últimos 5", style: { width: 'auto' } }, 
    ]

    const { actions } = useContext(Context)
    const [data, setData] = useState([])

    const loadData = async () => {
        const apiData = await actions.getStandings()
        setData(apiData)
    }

    useEffect(() => {
        loadData()
    }, [])

    return (
        <div className="container-fluid">
            <h1 className="text-center mt-3">Resultados</h1>
            <div className="container">
                <Table baseKey='standingsTable' headers={headers} footer={<LegendStandings />}>
                    <TableStandings data={data} />
                </Table>
            </div>
        </div>
    )
}

