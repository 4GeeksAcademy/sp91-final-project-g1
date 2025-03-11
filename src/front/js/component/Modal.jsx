import React from "react";
import Modal from 'react-bootstrap/Modal';
import PropTypes from "prop-types";
import { Button } from "react-bootstrap";

export const MyModal = (props) => {
    const handleClose = () => props.setShow(false);

    return (
        <Modal show={props.show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{props.modalData.title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>{props.modalData.body}</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Cancelar
                </Button>
                <Button variant={props.modalData.acceptButtonType} onClick={props.modalData.onAccept}>
                    {props.modalData.acceptButtonLabel}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

Modal.propTypes = {
    show: PropTypes.bool,
    setShow: PropTypes.func,
    modalData: PropTypes.object,
}