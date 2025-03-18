import React, { useContext, useEffect, useState } from "react"
import playerBg from "../../img/playerBg.png";
import PropTypes from "prop-types";
import { Context } from "../store/appContext";
import playerPlaceholder from '../../img/player-placeholder.png'


export const Player = (props) => {
    const player = props.player
    const size = props.isInBench ? 150 : 175
    const [processedImage, setProcessedImage] = useState(null);
    const { actions } = useContext(Context)
    const handleImageLoad = async () => {
        const processed = await actions.removeBgFromImage(player.photo);
        if (processed !== "ERROR") {
            setProcessedImage(processed);
        }
    };

    useEffect(() => {
        if (player.photo !== '') {
            handleImageLoad();
        }
        else {
            setProcessedImage(playerPlaceholder)
        }
    }, [player])

    return (
        <div className={`card text-white border-0`} style={{ width: `${size}px`, height: `${size}px` }}>
            <img className="card-img" src={playerBg} alt="Card image" />
            <div className={`card-img-overlay d-flex flex-column justify-content-center align-items-center ${player.isInBench && "p-0"}`}>
                <img src={processedImage} className="card-text " height={size * 0.4} width={size * 0.4} />
                <p className="card-title m-0">{player.name}</p>
                <p className={`card-text ${!player.isInBench && "fs-5"} m-0`}>{player.points}</p>
            </div>
        </div>
    )
}
Player.propTypes = {
    player: PropTypes.object,
    isInBench: PropTypes.bool,
}
Player.defaultProps = {
    player: {
        photo: '',
        name: '',
        points: 0
    },
    isInBench: false,
}
