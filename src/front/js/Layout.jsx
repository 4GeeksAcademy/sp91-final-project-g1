import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import injectContext from "./store/appContext";
// Custom Components
import { MyTeam } from "./pages/MyTeam.jsx";
import ScrollToTop from "./component/ScrollToTop.jsx";
import { BackendURL } from "./component/BackendURL.jsx";
import { Navbar } from "./component/Navbar.jsx";
import { Footer } from "./component/Footer.jsx";
// Custom Views
import { Login } from "./pages/Login.jsx";
import { MyLeague } from "./pages/MyLeague.jsx";
import { Standings } from "./pages/Standings.jsx";
import { Market } from "./pages/Market.jsx";
import { Settings } from "./pages/Settings.jsx";
import { ResetPassword } from "./pages/ResetPassword.jsx";
import { HomePage } from "./pages/HomePage.jsx";


// Create your first component
const Layout = () => {
    // The basename is used when your project is published in a subdirectory and not in the root of the domain
    // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
    const basename = process.env.BASENAME || "";
    if (!process.env.BACKEND_URL || process.env.BACKEND_URL == "") return <BackendURL />;

    return (
        <BrowserRouter basename={basename}>
            <ScrollToTop>
                <Navbar />
                <Routes>
                    <Route element={<HomePage />} path="/" />
                    <Route element={<Login />} path="/login" />
                    <Route element={<Standings />} path="/standings" />
                    <Route element={<MyTeam />} path="/my-team" />
                    <Route element={<MyLeague />} path="/my-league" />
                    <Route element={<Market />} path="/market" />
                    <Route element={<Settings />} path="/settings" />
                    <Route element={<ResetPassword />} path="/reset-password" />
                    <Route element={<h1>Not found!</h1>} path='*' />
                </Routes>
                <Footer />
            </ScrollToTop>
        </BrowserRouter>
    );
};

export default injectContext(Layout);
