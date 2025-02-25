import React, { useContext, useState, useEffect  } from "react"
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

export const Home = () => {
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
	
	const handleLogout =() =>{
		actions.logout()
		navigate("/")
	}
	return (
		<div className="text-center">
			<h1>Hola {userName}</h1>
			<button type="button" class="btn btn-outline-danger " onClick={handleLogout}>Logout</button>
		</div>
	);
};
