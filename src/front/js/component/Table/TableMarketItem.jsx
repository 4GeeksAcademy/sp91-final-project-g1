import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../store/appContext.js"
import PropTypes from "prop-types";
import { MyModal } from "../Modal.jsx";
import teamPlaceholder from '../../../img/team-placeholder.png'

export const TableMarketItem = (props) => {
    const { store, actions } = useContext(Context);
    const [imageUrl, setImageUrl] = useState("");
    const [isLoading, setIsLoading] = useState(true)
    const [modalData, setModalData] = useState({})
    const [showModal, setShowModal] = useState(false)

    const getImageWithoutBg = async () => {
        const image = await actions.removeBgFromImage(props.photo)
        setImageUrl(image)
        setIsLoading(false)
    }

    const fantasyTeam = actions.getFromLocalStorage('fantasyTeam')

    const handleScoutPlayer = () => {
        const data = {
            title: 'Fichar jugador',
            body: <span>¿Seguro que quieres fichar a <strong>{props.name}</strong> por {props.market_value.toLocaleString()}€?</span>,
            onAccept: async () => {
                const playerData = props

                const body = {
                    player_id: playerData.uid,
                    position: playerData.position,
                    clause_value: playerData.market_value,
                    fantasy_team_id: actions.getFromLocalStorage('fantasyTeam').id
                }
                const response = await actions.api.post("fantasy-players", body);
                if (response) {
                    setShowModal(false);
                    window.location.reload();
                }
            },
            acceptButtonType: 'primary',
            acceptButtonLabel: 'Fichar',
        }
        setModalData(data)
        setShowModal(true)
    }

    const POSITION_SELECT = [
        { label: 'PR', value: 'Goalkeeper', className: 'text-info goalkeeper' },
        { label: 'DF', value: 'Defender', className: 'text-success defender' },
        { label: 'MC', value: 'Midfielder', className: 'text-warning midfielder' },
        { label: 'DL', value: 'Attacker', className: 'text-danger forward' },
    ]
    const position = POSITION_SELECT.find(pos => pos.value === props.position)

    useEffect(() => {
        getImageWithoutBg()
    }, [])

    return (
        <>
            {fantasyTeam.id !== props.fantasy_team?.id &&
                <tr key={props.name}>
                    <td className="d-flex justify-content-between">
                        <div className="d-flex gap-2">
                            {
                                isLoading
                                    ?
                                    <i className="fa-solid fa-user px-2" style={{ fontSize: 158 }}></i>
                                    :
                                    <img src={imageUrl} alt="" />
                            }
                            <div className="d-flex flex-column gap-2" style={{ minWidth: 'fit-content' }}>
                                <p className="h4 w-100">{props.name}</p>
                                {
                                    <>
                                        <div className="d-flex gap-2 align-items-center">
                                            <img src={props.team.logo} alt="" width={20} height={20} />
                                            <span>{props.team.name}</span>
                                        </div>
                                        <div className="d-flex gap-2 align-items-center">
                                            {props.fantasy_team
                                                ?
                                                <>
                                                    <img src={props.fantasy_team.logo || teamPlaceholder} width={20} height={20} />
                                                    <span>{props.fantasy_team.name}</span>
                                                </>
                                                :
                                                <>
                                                    <i className="fa-solid fa-circle-xmark text-secondary"></i>
                                                    <span>Sin equipo</span>
                                                </>
                                            }
                                        </div>
                                    </>
                                }
                            </div>
                            <span className={`position ${position.className} fs-5`}>{position.label}</span>
                        </div>
                        {
                            <div className="d-flex flex-column gap-2 align-items-end mt-4 pt-1">
                                <div className="d-flex flex-column gap-2">
                                    <div className="d-flex gap-1">
                                        <span className="text-secondary">Precio</span>
                                        <span>{props.market_value.toLocaleString()}</span>
                                    </div>
                                </div>
                                <button className="btn btn-primary mt-auto px-3" onClick={handleScoutPlayer}>
                                    Fichar
                                </button>
                                <MyModal show={showModal} setShow={setShowModal} modalData={modalData} />
                            </div>
                        }
                    </td>
                </tr>
            }
        </>
    )
}

TableMarketItem.propTypes = {
    photo: PropTypes.string,
    name: PropTypes.string,
}
