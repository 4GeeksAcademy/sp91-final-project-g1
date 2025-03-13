import PropTypes from "prop-types";
import React from "react";
import { TableMarketItem } from "./TableMarketItem.jsx";

export const TableMarket = (props) => {
    return (
        <>
            {props.data?.map((item, index) => {
                return (<TableMarketItem key={index} {...item} />)
            })
            }
        </>
    )
}

TableMarket.propTypes = {
    data: PropTypes.array
}

TableMarket.defaultProps = {
    data: []
}