import React, { useContext, useRef, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { Login } from "../component/Login.jsx";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<Login />
	)
};
