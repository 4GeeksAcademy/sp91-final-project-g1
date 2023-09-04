import React from "react";

const Cards=(props)=>{
  return(
    <div className="card mb-3">
    <div className="row g-0">
      <div className="col-md-4">
        <div  style={{ position:"absolute", width:"9%",height:"19%" ,top:"3%",left:"1%", backgroundColor:"black", opacity: "0.5" }} className={props.day}>
           <p  style={{color:"white"}}> 25</p>
           <p  style={{color:"white"}}> Dec</p>

           
        </div>
        <img src={props.src} className="img-fluid rounded-start" alt="photo the basket"/>
      </div>
      <div className="col-md-8">
        <div className="card-body">
          <h5 className="card-title">{props.title}</h5>
          <p> <i className="bi bi-clock"></i>{props.time}<i className="bi bi-geo-alt-fill"></i>  {props.location}</p>
          <p className="ca rd-text">{props.description}</p>
          <p className="card-text"><small className="text-body-secondary">{props.lastUpdated}</small></p>
          <button id="click">REGISTRO</button>
        </div>
      </div>
    </div>
  </div>


   
  );
}
export default Cards;