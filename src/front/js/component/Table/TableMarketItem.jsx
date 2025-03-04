import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../store/appContext.js"
import PropTypes from "prop-types";

export const TableMarketItem = (props) => {
    const { actions } = useContext(Context);
    const [imageUrl, setImageUrl] = useState("");
    const [isLoading, setIsLoading] = useState(true)

    const getImageWithoutBg = async() => {
        const image = await actions.removeBgFromImage(props.photo)
        setImageUrl(image)
        setIsLoading(false)
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
                                /**
                            <div className="d-flex gap-2 align-items-center">
                                <img src={props.team.logo} alt="" width={20} height={20}/>
                                <span>{props.team.name}</span>
                            </div>
                                <div className="d-flex gap-2 align-items-center">
                                {props.fantasyTeam 
                                ? 
                                    <>
                                        <img src={props.fantasyTeam.logo} width={20} height={20}/>
                                        <span>{props.fantasyTeam.name}</span>
                                    </>
                                :
                                    <>
                                        <i className="fa-solid fa-circle-xmark text-secondary"></i>
                                        <span>Sin equipo</span>
                                    </>
                                }
                            </div>
                             */
                            }
                        </div>
                        <span className={`position ${position.className} fs-5`}>{position.label}</span>
                    </div>
                    {
                        /**
                    <div className="d-flex flex-column gap-2 align-items-end">
                        <div className="d-flex align-items-baseline gap-1">
                            <span className="text-secondary">PFSY</span>
                            <span className="fs-2">{props.points}</span>
                        </div>

                        <div className="d-flex flex-column gap-2">
                            <div className="d-flex gap-1">
                                <span className="text-secondary">Precio</span>
                                <span>{props.marketValue.toLocaleString()}</span>
                            </div>
                        </div>

                        {props.clauseValue && 
                        <div className="d-flex flex-column gap-2">
                            <div className="d-flex gap-1">
                                <span className="text-secondary">Cláusula</span>
                                <span>{props.clauseValue.toLocaleString()}</span>
                            </div>
                        </div>
                        }
                        <button className="btn btn-primary mt-auto px-3">Fichar</button>
                    </div>
                     */
                    }
                </td>
            </tr>
    )
}

TableMarketItem.propTypes = {
    photo: PropTypes.string,
    name: PropTypes.string,
}