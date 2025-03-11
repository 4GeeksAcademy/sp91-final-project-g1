import React from "react";
import home from "../../img/home.png";
import { useNavigate } from "react-router-dom";

const CustomSplitText = ({ text, delay }) => {
    return (
        <div>
            {text.split("").map((char, index) => (
                <span
                    key={index}
                    style={{
                        display: "inline-block",
                        animation: `fadeIn 0.5s ${index * delay}s forwards`,
                        opacity: 0,
                    }}
                >
                    {char === " " ? "\u00A0" : char} 
                </span>
            ))}
        </div>
    );
};

export const HomePage = () => {
    const navigate = useNavigate();

    return (
        <div style={{ display: "flex", justifyContent: "center", alignItems: "flex-start", height: "100vh", paddingTop: "3%", position: "relative", background: "linear-gradient(to right, #FF4B2B, #FF416C)" }}>
            <div style={{ fontSize: "4rem", fontWeight: "bold", textAlign: "center", color: "white" }}>
                <CustomSplitText text="¡Bienvenido a 4Fantasy!" delay={0.1} />
            </div>
            <div style={{ position: "absolute", bottom: "0", left: "0px" }}>
                <img src={home} alt="Foto jugadores" style={{ width: "650px", height: "500px" }} />
            </div>
            <div style={{ position: "absolute", top: "50%", right: "200px", textAlign: "right" }}>
                <p style={{ fontSize: "1.5rem", fontWeight: "bold", color: "white", marginBottom: "10px" }}>
                    "La emoción del fútbol comienza aquí. <br /> ¡Forma tu equipo y compite ahora!"
                </p>
                <button type="button" className="btn btn-success mt-3" onClick={() => navigate('/login')} style={{ fontWeight: "bold", position: "absolute", top: "110%", left: "170px"}}>Empezar</button>
            </div>
        </div>
    );
};

const styles = `
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;

const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = styles;
document.head.appendChild(styleSheet);