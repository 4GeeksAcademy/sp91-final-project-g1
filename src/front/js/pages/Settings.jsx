import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import perfil from "../../img/perfil.png";
import { MyModal as Modal } from "../component/Modal.jsx";
import { MyAlert as Alert } from "../component/Alert.jsx";


export const Settings = () => {

    const { actions } = useContext(Context);
    const [userName, setUserName] = useState("");
    const [email, setEmail] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");

    const [modalData, setModalData] = useState({ title: "", body: "", onAccept: () => { }, acceptButtonLabel: "", acceptButtonType: "primary" })
    const [showModal, setShowModal] = useState(false);

    const [alertData, setAlertData] = useState({ body: "", variant: "" })
    const [showAlert, setShowAlert] = useState(false);

    const navigate = useNavigate()
    const handleShow = () => setShowModal(true);

    const handleShowSaveChanges = () => {
        const data = {
            title: "Guardar datos",
            body: "¿Deseas guardar los datos cambiados?",
            onAccept: () => {
                const userData = {
                    username: userName,
                    email: email,
                    phone_number: phoneNumber,
                };
                actions.updateUser(userData);
                setShowModal(false);
            }, 
            acceptButtonLabel: "Guardar cambios",
            acceptButtonType: "success"
        }
        setModalData(data)
        handleShow()
    }

    const handleShowDeleteAccount = () => {
        const data = {
            title: "Eliminar cuenta",
            body: <p>¿Estás seguro de que deseas eliminar tu cuenta? <strong>Esta opción es irreversible y se eliminarán tus datos.</strong></p>,
            onAccept: () => {
                actions.deleteUser();
                navigate('/')
            },
            acceptButtonLabel: "Eliminar",
            acceptButtonType: "danger"
        }
        setModalData(data)
        handleShow()
    }

    const handleResetPassword = () => {
        navigate("/reset-password");
    }

    useEffect(() => {
        const user = actions.getFromLocalStorage("user")
        setUserName(user.username)
        setEmail(user.email)
        setPhoneNumber(user.phone_number)
    }, [])

    return (
        <div className="container-fluid text-center mt-4">
            <Alert
                showAlert={showAlert}
                alertData={alertData}
            />
            <div className="d-flex align-items-center justify-content-between mx-2">
                <div className="d-flex align-items-center gap-5">
                    <img src={perfil} alt="Foto perfil" style={{ width: "100px", height: "100px" }} />
                    <h1>Hola, {userName}</h1>
                </div>
                <button type="button" className="btn btn-outline-danger">Cerrar sesión</button>
            </div>
            <form action="submit" className={`col-12 col-md-6 col-lg-4 d-flex flex-column gap-2 mx-auto needs-validation`} noValidate>
                <div className="form-group d-flex align-items-center gap-2 mt-3">
                    <label htmlFor="formGroupExampleInput" className="fw-bold w-25 text-end me-3">Username</label>
                    <input type="text" className="form-control" placeholder="Username" value={userName} onChange={(e) => setUserName(e.target.value)} required />
                    <div className="invalid-feedback">Please enter a valid new username</div>
                </div>
                <div className="form-group d-flex align-items-center gap-2 mt-3">
                    <label htmlFor="formGroupExampleInput2" className="fw-bold w-25 text-end me-3">Email</label>
                    <input type="email" className="form-control" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    <div className="invalid-feedback">Please enter a valid new email</div>
                </div>
                <div className="form-group d-flex align-items-center gap-2 mt-3">
                    <label htmlFor="formGroupExampleInput2" className="fw-bold w-25 text-end me-3">Phone number</label>
                    <input type="text" className="form-control" placeholder="Phone number" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} required />
                    <div className="invalid-feedback">Please enter a valid new phone number</div>
                </div>
                <button type="button" className="btn btn-info mt-3" onClick={handleShowSaveChanges}>Guardar cambios</button>
                <div className="d-flex flex-column align-items-center gap-3 mt-5" >
                    <button type="button" className="btn btn-warning w-100" onClick={handleResetPassword}>Restablecer contraseña</button>
                    <button type="button" className="btn btn-danger w-100" onClick={handleShowDeleteAccount}>Eliminar cuenta</button>
                </div>
            </form>
            <Modal
                show={showModal}
                setShow={setShowModal}
                modalData={modalData}
            />
        </div>
    )
}
