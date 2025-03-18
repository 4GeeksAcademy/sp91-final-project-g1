import PropTypes from "prop-types";
import React from "react";
import { Pagination as BsPagination } from "react-bootstrap";

export const Pagination = (props) => {

    const generatePage = (page) => {
        if (page > 0 && page * 15 < props.pagingData.total + 14) {
            return <BsPagination.Item onClick={() => props.setPage(page)}>
                {page}
            </BsPagination.Item>
        }
    }
    return (
        <BsPagination>
            <BsPagination.Prev disabled={props.page === 1} onClick={() => props.setPage(props.page - 1)} />

            {generatePage(props.page - 2)}
            {generatePage(props.page - 1)}
            <BsPagination.Item key={props.page} active>
                {props.page}
            </BsPagination.Item>
            {generatePage(props.page + 1)}
            {generatePage(props.page + 2)}

            <BsPagination.Next onClick={() => props.setPage(props.page + 1)} disabled={props.pagingData.count === props.pagingData.total} />

        </BsPagination>
    )
}

Pagination.propTypes = {
    page: PropTypes.number,
    setPage: PropTypes.func,
    pagingData: PropTypes.object
}
