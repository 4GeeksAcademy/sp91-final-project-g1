import React from "react";
import Alert from 'react-bootstrap/Alert';
import PropTypes from "prop-types";

export const MyAlert = (props) => {

    return (
        <>
            {
                props.showAlert && <Alert key={props.alertData.variant} variant={props.alertData.variant}>
                    {props.alertData.body}
                </Alert>
            }
        </>
    )
}

MyAlert.propTypes = {
    showAlert: PropTypes.boolean,
    alertData: PropTypes.object,
}

MyAlert.defaultProps = {
    alertData: {
        variant: "primary",
    }
}