import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { Navigate, Outlet } from "react-router-dom";

export const ProtectedPages = () => {
    const { store } = useContext(Context)

    return store.user ? <Outlet /> : <Navigate to="/" />;
};