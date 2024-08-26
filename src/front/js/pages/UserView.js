import React from 'react';
import UsersProfile from '../component/userview/UsersProfile';
import UserDescription from '../component/userview/UserDescripcion';
import { EditDescriptionUserAccordion } from '../component/userview/DescriptionUserAccordion';
import UserExperience from '../component/userview/UserExperience';
import UserLenguages from '../component/userview/UserLenguages';
import UserFavs from '../component/userview/UserFavs';
import {EditFavoritesUserAccordion} from '../component/userview/FavsUserAccordion';
import {EditLanguageUserAccordion} from '../component/userview/lenguagesUserAccordion';
import {EditExperienceUserAccordion} from '../component/userview/experinceUserAccordion';
import '../../styles/userview.css';

export const Userview = () => {
    return (

        <div className="container">
            <div className='body'>
            <UsersProfile />


                <UserDescription title="Descripción">
                    <EditDescriptionUserAccordion />
                </UserDescription>

                <UserExperience title="Experiencia">
                    <EditExperienceUserAccordion />
                </UserExperience> 

                <UserFavs title="Favs">
                    <EditFavoritesUserAccordion />
                </UserFavs>   

                <UserLenguages title="Idiomas">
                    <EditLanguageUserAccordion />
                </UserLenguages>               
                   

                
                
            </div>
        </div>

    )
};


