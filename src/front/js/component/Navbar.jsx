import React, { useContext } from "react";
import { Link } from "react-router-dom";
import logo from "../../img/logo.png"
import { Context } from "../store/appContext";

export const Navbar = () => {
	const { actions } = useContext(Context)
	const user = actions.getFromLocalStorage("user")

	return (
		<nav className="navbar bg-body-tertiary">
			<div className="container-fluid d-flex align-items-center">
				<Link to={'/'} className="navbar-brand me-auto ms-5">
					<img src={logo} alt="Logo" width="50" />
				</Link>
				<div className="d-flex justify-content-center flex-grow-1">
					<ul className="navbar-nav d-flex flex-row gap-5">
						<li className="nav-item">
							<Link className="nav-link" to="/standings">
								Resultados
							</Link>
						</li>
						{user && (
							<>
								<li className="nav-item">
									<Link className="nav-link" to="/my-team">
										Mi equipo
									</Link>
								</li>
								<li className="nav-item">
									<Link className="nav-link" to="/my-league">
										Mi liga
									</Link>
								</li>
								<li className="nav-item">
									<Link className="nav-link" to="/market">
										Mercado
									</Link>
								</li>
							</>
						)}
					</ul>
				</div>
				<div className="ms-auto me-5">
					{user && (
						<Link to="/settings" className="nav-link">
							<i className="fa-solid fa-user fa-lg"></i>
						</Link>
					)}
				</div>
			</div>
		</nav>
	);
};
