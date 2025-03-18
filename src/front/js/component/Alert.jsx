import React from "react";
import Alert from 'react-bootstrap/Alert';
import PropTypes from "prop-types";

export const MyAlert = (props) => {

    return (
        <>
            {
                props.showAlert && <Alert key={props.alertData.variant} variant={props.alertData.variant} dismissible onClose={() => props.setShowAlert(false)}>
                    {props.alertData.body}
                </Alert>
            }
        </>
    )
}

MyAlert.propTypes = {
    showAlert: PropTypes.bool,
    setShowAlert: PropTypes.func,
    alertData: PropTypes.object,
}

MyAlert.defaultProps = {
    alertData: {
        variant: "primary",
    }
}
