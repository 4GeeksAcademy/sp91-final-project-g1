import React, {useContext, useState} from "react"
import playerBg from "../../img/playerBg.png";
import PropTypes from "prop-types";
import { Context } from "../store/appContext";


export const Player = (props) => {
    const size = props.isInBench ? 150 : 175
    const [processedImage, setProcessedImage] = useState(null);
    const { actions } = useContext (Context)    
    const handleImageLoad = async () => {
        if (props.photo) {
            const processed = await actions.removeBgFromImage(props.photo);
            if (processed !== "ERROR") {
                setProcessedImage(processed);
            }
        }
    };

    if (props.photo) {
        handleImageLoad();
    }
    
    return ( 
        <div className={`card text-white border-0`} style={{ width: `${size}px`, height: `${size}px` }}>
            <img className="card-img" src={playerBg} alt="Card image" />
            <div className={`card-img-overlay d-flex flex-column justify-content-center align-items-center ${props.isInBench && "p-0"}`}>
                <img src={processedImage || props.photo} className="card-text " height={size * 0.4} width={size * 0.4} />
                <p className="card-title m-0">{props.name}</p>
                <p className={`card-text ${!props.isInBench && "fs-5"} m-0`}>{props.points}</p>
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
