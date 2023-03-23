import React, { useContext, useEffect, useState } from "react";
import { Context } from "../store/appContext.js";
import { Container, Row, Col, Button } from "react-bootstrap";
import GameCard from "../component/GameCard.jsx";
import "../../styles/home.css";
import { Slide } from "react-slideshow-image";
import "react-slideshow-image/dist/styles.css";
import GameData from "../component/GameAPI.jsx";

const Home = () => {
  const { store, actions } = useContext(Context);
  const [games, setGames] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    GameData().then((data) => setGames(data));
  }, []);

  const slideImages = games.slice(0, 5).map((game) => game.header_image);

  const properties = {
    duration: 5000,
    transitionDuration: 500,
    infinite: true,
    indicators: true,
    arrows: true,
  };

  const handleSearch = (event) => {
    setSearchQuery(event.target.value);
  };

  return (
    <div className="home-container">
      <div className="hero-container">
        <Container>
          <Row className="align-items-center">
            <Col md={6} className="order-md-1">
              <h1>Welcome to My Game Store</h1>
              <p className="lead">
                Find your favorite games and discover new ones, all in one
                place.
              </p>
              <Button variant="primary">Explore games</Button>
            </Col>
            <Col md={6} className="order-md-2">
              <div className="slide-container">
                <Slide {...properties}>
                  {slideImages.map((each, index) => (
                    <div key={index} className="each-slide">
                      <img src={each} alt="slide" />
                    </div>
                  ))}
                </Slide>
              </div>
            </Col>
          </Row>
        </Container>
      </div>
      <Container>
        <Row className="my-5">
          <Col>
            <h2>Top Games</h2>
          </Col>
          <Col className="text-end">
            <Button variant="link" className="text-decoration-none">
              View All
            </Button>
          </Col>
          <Col md={4} className="ms-auto">
            <input
              type="text"
              className="form-control"
              placeholder="Search games"
              value={searchQuery}
              onChange={handleSearch}
            />
          </Col>
        </Row>
        <Row>
          {games
            .filter(
              (game) =>
                searchQuery.trim() === "" ||
                game.title.toLowerCase().includes(searchQuery.toLowerCase())
            )
            .map((game, index) => (
              <GameCard
                key={index}
                title={game.title}
                imageUrl={game.imageUrl}
                final_price={game.final_price}
                
              />
            ))}
        </Row>
      </Container>
    </div>
  );
};

export default Home;
