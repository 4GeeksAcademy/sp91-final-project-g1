import PropTypes from "prop-types"
import React, { useContext, useState } from "react"
import { Context } from "../../store/appContext"
import { checkFormValidity } from "../../utils"

export const LoginForm = (props) => {

    const { actions } = useContext(Context)
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleLogin = (event) => {
        event.preventDefault()
        if (!checkFormValidity(event)) return

        const body = { email, password }
        actions.login(body)
    }

    return (
        <div className={`col-6 d-flex justify-content-center sign-form ${props.isLoginActive && 'active'}`}>
            <form action="submit" onSubmit={handleLogin} className={`col-12 col-md-6 col-lg-4 d-flex flex-column gap-2 align-center needs-validation`} noValidate>
                <h1>Sign in</h1>
                <div>
                    <input className="form-control" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required/>
                    <div className="invalid-feedback">Please enter a valid email</div>
                </div>
                <div>
                    <input className="form-control" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required/>
                    <div className="invalid-feedback">Please enter a valid password</div>
                </div>
                <a href="#">Forgot your password?</a>
                <button className="btn btn-primary rounded-pill px-4 py-2 m-auto">Sign In</button>
            </form>
        </div>
    )
}

LoginForm.propTypes = {
    isLoginActive: PropTypes.bool
}
