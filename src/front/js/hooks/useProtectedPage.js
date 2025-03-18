import { useState, useEffect, useContext } from "react"
import { useNavigate } from "react-router-dom"
import { Context } from "../store/appContext"

export const useProtectedPage = () => {
    const navigate = useNavigate()
    const { actions } = useContext(Context)
    const [userData, setUserData] = useState(null)

    useEffect(() => {
        const user = actions.getFromLocalStorage("user");
        if (!user) {
            navigate("/")
            return
        }
        setUserData(user)
    }, [])
    return userData
}
