import React, { useContext, useState } from "react";
import { Table } from "../component/Table/Table.jsx";
import { TableStandings } from "../component/Table/TableStandings.jsx";
import { MyModal } from "../component/Modal.jsx";
import { Context } from "../store/appContext.js";

export const MyLeague = () => {
    const [showModal, setShowModal] = useState(false);
    const [modalData, setModalData] = useState({});
    const [leagueId, setLeagueId] = useState("");  
    const [nameTeam, setNameTeam] = useState("");
    const [logo, setLogo] = useState("");
    const [data, setData] = useState([]);  
    const { actions } = useContext(Context)
    
    const headers = [
        { label: "#", style: { width: '20px' } },
        { label: "Club", style: { width: '200px' } },
        { label: "GF", style: { width: 'auto' } },
        { label: "TA", style: { width: 'auto' } },
        { label: "TR", style: { width: 'auto' } },
        { label: "Puntos", style: { width: 'auto' } },
    ];
    const handleAddteam = () =>{
        
    }
    const handleJoinLeague = () => {
        setModalData({
            title: "Unirse a liga",
            body: (
                <form action="submit" className={`col-12 col-md-6 col-lg-4 d-flex flex-column gap-2 align-center needs-validation`} noValidate>
                    <div>
                        <label htmlFor="id" className="form-label fw-bold">Id</label>
                        <input className="form-control" type="number" placeholder="ID" value={leagueId} onChange={(e) => setLeagueId(e.target.value)} required />
                    </div>
                    <div>
                        <label htmlFor="Name-Team" className="form-label fw-bold">Name Team</label>
                        <input className="form-control" type="text" placeholder="Name-Team" value={nameTeam} onChange={(e) => setNameTeam(e.target.value)} required />
                    </div>
                    <div>
                        <label htmlFor="logo" className="form-label fw-bold">Logo</label>
                        <input className="form-control" type="text" placeholder="Logo" value={logo} onChange={(e) => setLogo(e.target.value)} />
                    </div>
                </form>
            ),
            onAccept: async () => {
                // TODO: No funciona correctamente nos falta datos de usuario
                const newTeam = {
                    id: leagueId,         
                    nameTeam: nameTeam,   
                    logo: logo,         
                };
                await actions.addTeam(newTeam)
                setData([...data, newTeam]);
                setLeagueId("");
                setNameTeam("");
                setLogo("");
                setShowModal(false);
            },
            acceptButtonLabel: "Unirse a la liga",
            acceptButtonType: "success",
        });
        setShowModal(true);
    };

    return (
        <div className="container-fluid">
            <div className="d-flex gap-3 justify-content-center align-items-center">
                <h1 className="text-center">Mi liga</h1>
                <button className="btn btn-outline-primary" onClick={handleAddteam}>Añadir equipo</button>
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
                            <button className="btn btn-primary px-3" onClick={handleJoinLeague}>Unirse a liga</button>
                        </div>
                }
            </div>
            <MyModal show={showModal} setShow={setShowModal} modalData={modalData} />
        </div>
    );
}