import React, { useContext, useState, useEffect } from "react"
import { Context } from "../store/appContext";
import { LineUp } from "../component/LineUp.jsx";
import { Bench } from "../component/Bench.jsx";
import { TeamData } from "../component/TeamData.jsx";
import { Overlay } from "../component/Overlay.jsx";
import { useProtectedPage } from "../hooks/useProtectedPage.js";

export const MyTeam = () => {
	const [hasLeague, setHasLeague] = useState(false);
	const { actions } = useContext(Context);
	const user = useProtectedPage();
    const getUserTeam = async () => {
		if (user) {
		  try {
			const userHasTeam = await actions.getUserTeam(user.id) !== null;  
			setHasLeague(userHasTeam); 
		  } catch (error) {
			console.error("Error al obtener el equipo del usuario:", error);
		  }
		}
	  };

	  useEffect(() => {
		if (user) {
		  getUserTeam(user.id);  
		}
	  }, [user]); 

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
)};