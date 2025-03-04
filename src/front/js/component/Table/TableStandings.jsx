import PropTypes from "prop-types";
import React from "react";

export const TableStandings = (props) => {

    const setSpecialPositionBorder = (index) => {
        switch (true) {
            case index <= 3:
                return "text-info"
            case index === 4:
                return "text-warning"
            case index === 5:
                return "text-success"
            case index >= 17:
                return "text-danger"
            default:
                break;
        }
    }

    return (
        <>
            {props.data.map((item, index) => {
                return (
                    <tr key={index}>
                        <th className={setSpecialPositionBorder(index)}>{index + 1}</th>
                        {Object.entries(item).map(([key, itemData]) => {
                            if(key === "team") {
                                return (
                                    <td>
                                        <div className="d-flex gap-2 align-items-center">
                                            <img src={itemData.logo} alt={`${itemData.name}'s logo`} width={20} height={20}/>
                                            <span>{itemData.name}</span>
                                        </div>
                                    </td>
                                )
                            }
                            if(key === "form") {
                                return (
                                <td className="">
                                    {itemData.split("").map((matchResult) => {
                                        switch (matchResult) {
                                            case "V":
                                                return <i className="fa-solid fa-circle-check text-success pe-1"></i>
                                            case "D":
                                                return <i className="fa-solid fa-circle-xmark text-danger pe-1"></i>
                                            default:
                                                return <i className="fa-solid fa-circle-minus text-secondary pe-1"></i>
                                        }
                                    })}
                                </td>
                                )
                            }
                            return (
                                <td>{itemData}</td>
                            )
                        })}
                    </tr>
                )
            })}
        </>
    )
}

TableStandings.propTypes = {
    data: PropTypes.array
}

TableStandings.defaultProps = {
    data: []
}