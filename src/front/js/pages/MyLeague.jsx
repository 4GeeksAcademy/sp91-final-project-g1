import React, { useContext, useState } from "react";
import { Table } from "../component/Table/Table.jsx";
import { TableStandings } from "../component/Table/TableStandings.jsx";
import { Context } from "../store/appContext.js";
import { useProtectedPage } from "../hooks/useProtectedPage.js";
import { Button, Modal } from "react-bootstrap";

export const MyLeague = () => {
    const [showModal, setShowModal] = useState(false);
    const [modalData, setModalData] = useState({});
    const [leagueId, setLeagueId] = useState("");  
    const [teamName, setTeamName] = useState("");
    const [logo, setLogo] = useState("");
    const [data, setData] = useState([]);  
    const { actions } = useContext(Context)
    const user = useProtectedPage();

    const handleClose = () => setShowModal(false);
    const onAccept = async () => {
        const newTeam = {
            fantasy_league_id: leagueId,     
            user_id: user?.id,    
            name: teamName,
            logo: logo,         
        };
        await actions.addTeam(newTeam)
        /* setData([...data, newTeam]);
        setLeagueId("");
        setNameTeam("");
        setLogo(""); */
        setShowModal(false);
    }

    const headers = [
        { label: "#", style: { width: '20px' } },
        { label: "Club", style: { width: '200px' } },
        { label: "GF", style: { width: 'auto' } },
        { label: "TA", style: { width: 'auto' } },
        { label: "TR", style: { width: 'auto' } },
        { label: "Puntos", style: { width: 'auto' } },
    ];
    const handleAddteam = () =>{
        // TODO: Añadir funcionalidad
    }
    const handleJoinLeague = () => {
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
            <Modal show={showModal} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Unirse a liga</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <form className={`col-12 col-md-6 col-lg-4 d-flex flex-column gap-2 align-center needs-validation`} noValidate>
                    <div>
                        <label htmlFor="id" className="form-label fw-bold">Id</label>
                        <input name="id" className="form-control" type="number" placeholder="ID" value={leagueId} onChange={(e) => setLeagueId(e.target.value)} required />
                    </div>
                    <div>
                        <label htmlFor="teamName" className="form-label fw-bold">Team name</label>
                        <input name="teamName" className="form-control" type="text" placeholder="Team name" value={teamName} onChange={(e) => setTeamName(e.target.value)} required />
                    </div>
                    <div>
                        <label htmlFor="logo" className="form-label fw-bold">Logo</label>
                        <input name="logo" className="form-control" type="text" placeholder="Logo" value={logo} onChange={(e) => setLogo(e.target.value)} />
                    </div>
                </form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Cancelar
                </Button>
                <Button variant='success' onClick={onAccept}>
                    Unirse a la liga
                </Button>
            </Modal.Footer>
        </Modal>
        </div>
    );
}