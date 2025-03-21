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
    const [pagingData, setPagingData] = useState({
        total: 0,
        count: 0
    })

    const getPlayers = async () => {
        setIsLoading(true)
        const playersData = await actions.api.get('players-market', `page=${page - 1}&limit=15`)

        setData(playersData.results)
        setPagingData({
            total: playersData.total,
            count: playersData.count
        })
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
                <Pagination page={page} setPage={setPage} pagingData={pagingData} />
            </div>
        </div>
    )
}
