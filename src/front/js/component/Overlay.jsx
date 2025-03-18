import React from "react"
import { useNavigate } from "react-router-dom";

export const Overlay = () => {
    const navigate = useNavigate();

    const handleJoin = async () => {
        navigate("/my-league")
    };

    return (
        <div className="backdrop w-100 h-100 z-1 position-absolute d-flex flex-column align-items-center justify-content-center">
            <p>No tienes liga aún, créate una y únete a nosotros</p>
            <button onClick={handleJoin} className="btn btn-primary rounded" type="button">Únete</button>
        </div>
    )
}
