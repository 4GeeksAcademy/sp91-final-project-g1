import React, { useState } from "react";
import "../../styles/login.css";
import { LoginForm } from "../component/Login/LoginForm.jsx";
import { SignupForm } from "../component/Login/SignupForm.jsx";
import { LoginSliderOverlays } from "../component/Login/LoginSliderOverlays.jsx";

export const Login = () => {
	const [isLoginActive, setIsLoginActive] = useState(true)

	return (
		<div className="row flex-grow-1 align-items-center">
			<LoginForm isLoginActive={isLoginActive} />
			<SignupForm isLoginActive={isLoginActive} />
			<LoginSliderOverlays isLoginActive={isLoginActive} setIsLoginActive={setIsLoginActive} />
		</div>
	)
};
