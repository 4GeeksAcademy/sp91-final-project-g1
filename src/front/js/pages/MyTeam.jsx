import React, { useContext, useState, useEffect } from "react"
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import { LineUp } from "../component/LineUp.jsx";
import { Bench } from "../component/Bench.jsx";
import { TeamData } from "../component/TeamData.jsx";
import { Overlay } from "../component/Overlay.jsx";

export const MyTeam = () => {
	const [hasLeague, setHasLeague] = useState(false);
	const { actions } = useContext(Context);
	const [userName, setUserName] = useState("");
	const navigate = useNavigate();

	useEffect(() => {
		const user = actions.getFromLocalStorage("user");
		if (!user) {
			navigate("/")
			return
		}
		setUserName(user.username)
	}, [])

	const handleLogout = () => {
		actions.logout()
		navigate("/")
	}
	return (
		<div className="container-fluid row">
		   {!hasLeague && <Overlay />} 
			<div className="col-4 mt-auto">
				<Bench />
			</div>
			<div className="col-6">
				<LineUp />
			</div>
			<div className="col-2">
				<TeamData />
			</div>
		</div>
	);
};
