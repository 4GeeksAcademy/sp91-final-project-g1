export const checkFormValidity = (event) => {
    const form = event.target

    if (!form.checkValidity()) {

        event.stopPropagation()
        form.classList.add("was-validated") 
        return false
    }
    return true
}