export function Login() {
    const handleChange = () => {
        
    }

    return(
        <form onSubmit={handleChange}>
            <div className="form-group">
                <label htmlFor="username">Имя пользователя:</label>
                <input type="text"/>
            </div>
        </form>
    )
}