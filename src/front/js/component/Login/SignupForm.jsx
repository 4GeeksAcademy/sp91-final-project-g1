import PropTypes from "prop-types"
import React, { useContext, useState } from "react"
import { Context } from "../../store/appContext"
import { checkFormValidity } from "../../utils"
import { useNavigate } from "react-router-dom"
import { MyAlert as Alert } from "../Alert.jsx"

export const SignupForm = (props) => {
    const { actions } = useContext(Context)
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [phoneNumber, setPhoneNumber] = useState("")
    const navigate = useNavigate()

    const [alertData, setAlertData] = useState({ body: "", variant: "" })
    const [showAlert, setShowAlert] = useState(false);

    const handleSignup = async (event) => {
        event.preventDefault()
        if (!checkFormValidity(event)) return

        const body = {
            username: username,
            email: email,
            password: password,
            phone_number: phoneNumber !== "" ? phoneNumber : null
        }
        const response = await actions.signup(body)
        if (response.ok) {
            setAlertData({
                body: "Cuenta creada correctamente",
                variant: "success"
            });
            navigate("/my-team")
        } else {
            setAlertData({
                body: "El usuario o el email ya están en uso",
                variant: "danger",
            });
        }
        setShowAlert(true);
    }

    return (
        <div className={`col-6 d-flex flex-column justify-content-center align-items-center sign-form ${!props.isLoginActive && 'active'}`}>
            <Alert
                showAlert={showAlert}
                alertData={alertData}
            />
            <form action="submit" onSubmit={handleSignup} className={`col-12 col-md-6 col-lg-4 d-flex flex-column gap-2 align-center needs-validation`} noValidate>
                <h1>Create Account</h1>
                <div>
                    <input className="form-control" type="text" placeholder="Username *" value={username} onChange={(e) => setUsername(e.target.value)} required />
                    <div className="invalid-feedback">Please enter a valid username</div>
                </div>
                <div>
                    <input className="form-control" type="email" placeholder="Email *" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    <div className="invalid-feedback">Please enter a valid email</div>
                </div>
                <div>
                    <input className="form-control" type="password" placeholder="Password *" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    <div className="invalid-feedback">Please enter a valid password</div>
                </div>
                <div>
                    <input className="form-control" type="text" placeholder="Phone number" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} />
                </div>
                <button className="btn btn-primary rounded-pill px-4 py-2 m-auto">Sign Up</button>
            </form>
        </div>
    )
}

SignupForm.propTypes = {
    isLoginActive: PropTypes.bool
}
