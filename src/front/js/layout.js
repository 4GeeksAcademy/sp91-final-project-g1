import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Home } from "./pages/home";
import { Login } from "./pages/login.js";
import { SignUp } from "./pages/signUp.js";
import { Player } from "./pages/playerInfo.js";
import { EditPlayer } from "./pages/editPlayerInfo.js";
import { HostProfile } from "./pages/hostProfile.js";
import { HostProfileEdit } from "./pages/hostProfileEdit.js";

import injectContext from "./store/appContext";

import { Navbar } from "./component/navbar";
import { Footer } from "./component/footer";
import { CreateTournament } from "./pages/createTournament.js";
import { TournamentList } from "./pages/tournamentList.js";
import { TournamentDetails } from "./pages/tournamentDetails.js";
import { EditTournamentForm } from "./component/tournamentEditForm.jsx";


//create your first component
const Layout = () => {
    //the basename is used when your project is published in a subdirectory and not in the root of the domain
    // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
    const basename = process.env.BASENAME || "";

    if (!process.env.BACKEND_URL || process.env.BACKEND_URL == "") return <BackendURL />;

    return (
        <BrowserRouter basename={basename}>
            <ScrollToTop>
                <div className="d-flex flex-column min-vh-100">
                    <Navbar />
                    <div className="flex-grow-1">
                        <Routes>
                            <Route element={<Home />} path="/" />
                            <Route element={<Home />} path="/home" />
                            <Route element={<Login />} path="/login" />
                            <Route element={<SignUp />} path="/signup" />
                            <Route element={<Player />} path="/player/profile" />
                            <Route element={<EditPlayer />} path="player/editProfile" />
                            <Route element={<TournamentList />} path="/tournaments" />
                            <Route element={<TournamentDetails />} path="/tournaments/:id" />
                            <Route element={<CreateTournament />} path="/create_tournament" />
                            <Route element={<EditTournamentForm />} path="/edit-tournament/:id"/>
                            <Route element={<HostProfile />} path="/host/profile" />
                            <Route element={<HostProfileEdit />} path="/host/editProfile" />
                            <Route element={<h1>Not found!</h1>} path="/single/:theid" />
                        </Routes>
                    </div>
                    <Footer />
                </div>
            </ScrollToTop>
        </BrowserRouter>
    );
};
export default injectContext(Layout);
