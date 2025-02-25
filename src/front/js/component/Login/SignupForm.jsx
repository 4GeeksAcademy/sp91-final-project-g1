import PropTypes from "prop-types"
import React, { useContext, useState } from "react"
import { Context } from "../../store/appContext"
import { checkFormValidity } from "../../utils"
import { useNavigate } from "react-router-dom"

export const SignupForm = (props) => {

    const { actions } = useContext(Context)
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [phoneNumber, setPhoneNumber] = useState("")
    const navigate = useNavigate()
    
    const handleSignup = async (event) => {
        event.preventDefault()
        if (!checkFormValidity(event)) return

        const body = { 
            username: username, 
            email: email, 
            password: password, 
            phone_number: phoneNumber
        }
        const response = await actions.signup(body)
        if (response.status === 200) {
            navigate("/home")
        }
    }

    return (
        <div className={`col-6 d-flex justify-content-center sign-form ${!props.isLoginActive && 'active'}`}>
            <form action="submit" onSubmit={handleSignup} className={`col-12 col-md-6 col-lg-4 d-flex flex-column gap-2 align-center needs-validation`} noValidate>
                <h1>Create Account</h1>
                <div>
                    <input className="form-control" type="text" placeholder="Username *" value={username} onChange={(e) => setUsername(e.target.value)} required/>
                    <div className="invalid-feedback">Please enter a valid username</div>
                </div>
                <div>
                    <input className="form-control" type="email" placeholder="Email *" value={email} onChange={(e) => setEmail(e.target.value)} required/>
                    <div className="invalid-feedback">Please enter a valid email</div>
                </div>
                <div>
                    <input className="form-control" type="password" placeholder="Password *" value={password} onChange={(e) => setPassword(e.target.value)} required/>
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