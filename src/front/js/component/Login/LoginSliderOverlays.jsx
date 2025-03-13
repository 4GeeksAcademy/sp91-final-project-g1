import PropTypes from "prop-types";
import React from "react";

export const LoginSliderOverlays = (props) => {
    return (
        <div className="d-flex align-items-center position-fixed overlay">
            <div className={`overlay background z-2 ${props.isLoginActive ? 'right' : 'left'}`}></div>
            <div className={`col-6 p-4 overlay-panel right h-100 d-flex flex-column justify-content-center align-items-center ${props.isLoginActive ? '' : 'visible'}`}>
                <div className="col-12 col-md-6">
                    <h1>Hello, Friend!</h1>
                    <p>Enter your personal details and start journey with us</p>
                    <button className="btn btn-outline-light rounded-pill px-4 py-2 mx-auto" onClick={() => props.setIsLoginActive(true)}>Sign In</button>
                </div>
            </div>
            <div className={`col-6 p-4 overlay-panel left h-100 d-flex flex-column justify-content-center align-items-center ${props.isLoginActive ? 'visible' : ''}`}>
                <div className="col-12 col-md-6">
                    <h1>Welcome Back!</h1>
                    <p>To keep connected with us please login with your personal info</p>
                </div>
                <button className="btn btn-outline-light rounded-pill px-4 py-2 mx-auto" onClick={() => props.setIsLoginActive(false)}>Sign Up</button>
            </div>
        </div>
    )
}

LoginSliderOverlays.propTypes = {
    isLoginActive: PropTypes.bool,
    setIsLoginActive: PropTypes.func
}
