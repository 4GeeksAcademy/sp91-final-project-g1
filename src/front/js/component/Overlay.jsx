import React, { useState, useContext } from "react"
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

export const Overlay = () => {
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false); 
    const [hasLeague, setHasLeague] = useState(false);
    const { actions } = useContext(Context);
    const checkUserLeague = async () => {

        const leagueData = await actions.getUserLeague();
        if (leagueData && leagueData.league) {
            setHasLeague(true);  
            setHasLeague(false);  
        }
    };

    if (!hasLeague) {
        checkUserLeague();
    }

    const handleJoin = async () => {
        navigate("/my-league") 
    };

    if (hasLeague) {
        return null;
    }
    
    return (
            <div className="backdrop w-100 h-100 z-1 position-absolute d-flex flex-column align-items-center justify-content-center">
                <p>No tienes liga aún, créate una y únete a nosotros</p>
                <button onClick={handleJoin}  disabled={isLoading} className="btn btn-primary rounded" type="button">Únete</button>
            </div>
    )
}