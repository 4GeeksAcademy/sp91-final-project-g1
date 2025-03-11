import PropTypes from "prop-types";
import React from "react";

export const Table = (props) => {

    return (
        <table className="table table-striped">
            <thead>
                <tr>
                    {props.headers.map((header) => {
                        return (
                            <th key={`${props.baseKey}-${header.label}`} style={header.style} scope="col">{header.label}</th>
                        )
                    })}
                </tr>
            </thead>
            <tbody>
                {props.children}
            </tbody>
            <tfoot>
                {props.footer}
            </tfoot>
        </table>
    )
}

Table.propTypes = {
    headers: PropTypes.array,
    footer: PropTypes.element
}

Table.defaultProps = {
    headers: [],
}
