import React, { useContext, useState, useEffect } from "react"
import { Context } from "../store/appContext";
import { LineUp } from "../component/LineUp.jsx";
import { Bench } from "../component/Bench.jsx";
import { TeamData } from "../component/TeamData.jsx";
import { Overlay } from "../component/Overlay.jsx";
import { useProtectedPage } from "../hooks/useProtectedPage.js";

export const MyTeam = () => {
	const [team, setTeam] = useState(null);
	const { actions } = useContext(Context);
	const user = useProtectedPage();
	const getUserTeam = async () => {
		const userTeam = await actions.getUserTeam(user.id);
		const [defendersCount, midFieldersCount, forwardsCount] = userTeam.formation.split('-')
		const setBench = (position, count) => {
			const players = userTeam.players.filter(element => element.position === position)
			for (let i = 0; i < players.length; i++) {
				players[i].isInBench = i + 1 > count
			}
		}
		setBench('Defender', defendersCount)
		setBench('Midfielder', midFieldersCount)
		setBench('Attacker', forwardsCount)
		setTeam(userTeam);
	};

	useEffect(() => {
		if (user) {
			getUserTeam(user.id);
		}
	}, [user]);

	return (
		<div className="container-fluid row">
			{
				!team ?
					<Overlay /> :
					<>
						<div className="col-4 mt-auto">
							<Bench data={team} />
						</div>
						<div className="col-6">
							<LineUp data={team} />
						</div>
						<div className="col-2">
							<TeamData team={team} />
						</div>
					</>
			}
		</div>
	)
};
