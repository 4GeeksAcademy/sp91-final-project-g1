import PropTypes from "prop-types";
import React from "react";
import { Pagination as BsPagination } from "react-bootstrap";

export const Pagination = (props) => {

    return (
        <BsPagination>
            <BsPagination.Prev disabled={props.page === 1} onClick={() => props.setPage(props.page - 1)} />

            <BsPagination.Item key={props.page} active>
                {props.page}
            </BsPagination.Item>
            {!props.isMaxData &&
                <>
                    <BsPagination.Item key={props.page + 1} onClick={() => props.setPage(props.page + 1)}>
                        {props.page + 1}
                    </BsPagination.Item>
                    <BsPagination.Item key={props.page + 2} onClick={() => props.setPage(props.page + 2)}>
                        {props.page + 2}
                    </BsPagination.Item>
                </>
            }

            <BsPagination.Next onClick={() => props.setPage(props.page + 1)} disabled={props.isMaxData} />

        </BsPagination>
    )
}

Pagination.propTypes = {
    page: PropTypes.number,
    setPage: PropTypes.func,
    isMaxData: PropTypes.bool
}
