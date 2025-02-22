import React, { useState } from "react";

export const Login = () => {

	const [isLoginActive, setIsLoginActive] = useState(true)

    return (
        <div className="row flex-grow-1 align-items-center">
        	<div className={`col-6 sign-form ${isLoginActive && 'active'}`}>
        		<form action="#" className="d-flex flex-column gap-2 align-center">
        			<h1>Sign in</h1>
        			<input className="form-control" type="email" placeholder="Email" />
        			<input className="form-control" type="password" placeholder="Password" />
        			<a href="#">Forgot your password?</a>
        			<button className="btn btn-primary rounded-pill px-4 py-2 m-auto">Sign In</button>
        		</form>
        	</div>
			<div className={`col-6 sign-form ${!isLoginActive && 'active'}`}>
        		<form action="#" className="d-flex flex-column gap-2 align-center">
        			<h1>Create Account</h1>
        			<span>or use your email for registration</span>
        			<input className="form-control" type="text" placeholder="Name" />
        			<input className="form-control" type="email" placeholder="Email" />
        			<input className="form-control" type="password" placeholder="Password" />
        			<button className="btn btn-primary rounded-pill px-4 py-2 m-auto">Sign Up</button>
				</form>
        	</div>
        	<div className="d-flex align-items-center position-fixed overlay">
				<div className={`overlay background z-2 ${isLoginActive ? 'right' : 'left'}`}></div>
				<div className={`col-6 p-4 overlay-panel right h-100 d-flex flex-column justify-content-center ${isLoginActive ? '' : 'visible'}`}>
        			<h1>Hello, Friend!</h1>
        			<p>Enter your personal details and start journey with us</p>
        			<button className="btn btn-outline-light rounded-pill px-4 py-2 mx-auto" onClick={() => setIsLoginActive(true)}>Sign In</button>
        		</div>
        		<div className={`col-6 p-4 overlay-panel left h-100 d-flex flex-column justify-content-center ${isLoginActive ? 'visible' : ''}`}>
        			<h1>Welcome Back!</h1>
        			<p>To keep connected with us please login with your personal info</p>
        			<button className="btn btn-outline-light rounded-pill px-4 py-2 mx-auto" onClick={() => setIsLoginActive(false)}>Sign Up</button>
        		</div>
        	</div>
        </div>
    )
}
