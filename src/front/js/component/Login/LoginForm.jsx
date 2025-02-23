import PropTypes from "prop-types"
import React, { useContext, useState } from "react"
import { Context } from "../../store/appContext"

export const LoginForm = (props) => {

    const { actions } = useContext(Context)
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleLogin = (event) => {
        event.preventDefault()
        const body = {
            email: email,
            password: password
        }

        const response = actions.login(body)
    }

    return (
        <div className={`col-6 d-flex justify-content-center sign-form ${props.isLoginActive && 'active'}`}>
            <form action="submit" onSubmit={handleLogin} className="col-12 col-md-6 col-lg-4 d-flex flex-column gap-2 align-center">
                <h1>Sign in</h1>
                <input className="form-control" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>
                <input className="form-control" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
                <a href="#">Forgot your password?</a>
                <button className="btn btn-primary rounded-pill px-4 py-2 m-auto">Sign In</button>
            </form>
        </div>
    )
}

LoginForm.propTypes = {
    isLoginActive: PropTypes.bool
}
