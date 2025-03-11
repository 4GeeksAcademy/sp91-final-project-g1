import React, { useContext, useEffect, useState } from "react";
import { Table } from "../component/Table/Table.jsx";
import { TableMarket } from "../component/Table/TableMarket.jsx";
import { Context } from "../store/appContext.js";
import { useProtectedPage } from "../hooks/useProtectedPage.js";
import { Pagination } from "../component/Pagination.jsx";

export const Market = () => {
    const { actions } = useContext(Context)
    const [data, setData] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const user = useProtectedPage();
    const [page, setPage] = useState(1)
    const [isMaxData, setIsMaxData] = useState(false)

    const getPlayers = async() => {
        setIsLoading(true)
        const playerData = await actions.api.get('players-market', `page=${page - 1}&limit=15`)
        setData(playerData)
        setIsMaxData(playerData.length < 15)
        setIsLoading(false)
    }

    useEffect(() => {
        getPlayers()
    }, [])

    useEffect(() => {
        getPlayers()
    }, [page])

    return (
        <div className="container-fluid">
            <h1 className="text-center">Mercado de fichajes</h1>
            <div className="container col-9 col-lg-6 col-xl-4">
                {!isLoading && 
                <Table headers={[]}>
                    <TableMarket data={data} />
                </Table>}
                <Pagination page={page} setPage={setPage} isMaxData={isMaxData} />
            </div>
        </div>
    )
}
