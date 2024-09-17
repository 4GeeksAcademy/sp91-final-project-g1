import React, { useContext, useEffect, useState } from "react";
import logo from "../../img/logo/logo-marca.png"
import { Context } from "../store/appContext.js";
import {CardGame} from "../component/game_selection/card_game.jsx"
export const GameSelection = () => {

    const { store, actions } = useContext(Context);
    const [name_game, setName_game] = useState("")
    const [selectedGames, setSelectedGames] = useState([])

    useEffect(() => {
        actions.getRecommendedGames_gameSelection(6)
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if(name_game.trim() !== "")
        {   
            actions.getGameByName_gameSelection(name_game)
        }
    }

    const handleCardClick = (game_id) => {
        const storedIds = JSON.parse(localStorage.getItem("selectedGameIds")) || [];
        let updatedIds = [...storedIds];

        if (updatedIds.includes(game_id)) {
            updatedIds = updatedIds.filter(id => id !== game_id);
        } else {
            updatedIds.push(game_id);
        }

        console.log(updatedIds)
        localStorage.setItem("selectedGameIds", JSON.stringify(updatedIds));
        setSelectedGames(updatedIds);
    }

    const anyGameSelected = selectedGames.length > 0;

    return(
        <div className="d-flex flex-column min-vh-100 pb-3" style={{backgroundColor: "#16171C", color: "#fff"}}>
            <img  src={logo} alt="Logo" style={{width: '40%', height: '80px', margin: '10px', objectFit: "contain"}} />
        <div className="container text-center my-auto mt-5">
            <div className="row justify-content-center align-items-center">
                <h2 className="mb-5 fw-bold">Choose a prefered game</h2>
                <div className="col-md-6 mb-3">
                <form class="d-flex" role="search" onSubmit={handleSearch}>
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" onChange={(e) => setName_game(e.target.value)}/>
                </form>
                </div>
                <div className="container">
                    <div className="row d-flex justify-content-center gallery">
                        {(store.searchedGames && store.searchedGames.length > 0 ? store.searchedGames : store.recommendedGames).map(game => 
                                <CardGame key={game.id} name={game.name} imagen={game.background_image} onClick={() => handleCardClick(game.id)} isSelected={selectedGames.includes(game.id)}/>
                        )}
                    </div>
                </div>
            </div>
        </div>
            <footer className="text-center py-3 my-4">
                <div className="d-flex justify-content-center gap-2 flex-wrap">
                    <button className="btn btn-prev"><i className="fa-solid fa-arrow-left me-2"></i>Back</button>
                    <button className="btn btn-next" disabled={!anyGameSelected}>Continue</button>
                </div>
            </footer>
        </div>
    )
}