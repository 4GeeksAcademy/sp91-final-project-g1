import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkFormValidity } from "../utils";
import { Context } from "../store/appContext";
import { MyAlert as Alert } from "../component/Alert.jsx";
import { useProtectedPage } from "../hooks/useProtectedPage.js";

export const ResetPassword = (props) => {
    const { actions } = useContext(Context)
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const navigate = useNavigate();

    const [alertData, setAlertData] = useState({ body: "", variant: "" })
    const [showAlert, setShowAlert] = useState(false);

    const user = useProtectedPage();

    const handleResetPassword = async (event) => {
        event.preventDefault()
        if (!checkFormValidity(event)) return;

        if (password !== confirmPassword) {
            setAlertData({
                body: "Las contraseñas no coinciden",
                variant: "danger",
            });
            setShowAlert(true);
            return;
        }

        const body = { password };

        const response = await actions.resetPassword(body)
        if (response.ok) {
            setAlertData({
                body: "Contraseña modificada correctamente",
                variant: "success"
            });
        } else {
            setAlertData({
                body: "Ha habido un error, inténtalo más tarde",
                variant: "danger",
            });
        };
        setShowAlert(true);
        setPassword("");
        setConfirmPassword("");
        navigate('/settings')
    }

    return (
        <div className={`d-flex flex-column justify-content-center my-auto sign-form ${!props.ResetPassword && 'active'}`}>
            <Alert
                showAlert={showAlert}
                setShowAlert={setShowAlert}
                alertData={alertData}
            />
            <form action="submit" onSubmit={handleResetPassword} className={`col-12 col-md-6 col-lg-4 d-flex flex-column gap-2 mx-auto needs-validation`} noValidate>
                <h1>Nueva contraseña</h1>
                <div className="form-group d-flex flex-column align-items-center gap-2 mt-3">
                    <input type="password" className="form-control" placeholder="Nueva Contraseña" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    <div className="invalid-feedback">Por favor introduzca una contraseña válida</div>
                </div>
                <div className="form-group d-flex flex-column align-items-center gap-2 mt-3">
                    <input type="password" className="form-control" placeholder="Confirma Nueva Contraseña" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
                    <div className="invalid-feedback">Por favor confirma tu nueva contraseña</div>
                </div>
                <button type="submit" className="btn btn-info mt-3">Cambiar contraseña</button>
            </form>
        </div>
    )
}
