import { useState } from "react"
import { useNavigate } from "react-router-dom"

export const useProtectedPage = () => {
    const navigate = useNavigate()
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