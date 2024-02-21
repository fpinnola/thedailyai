import { useState } from "react";
import { login } from "./external/news_be.external";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleLogin = async (event: any) => {
        event.preventDefault();
        setIsLoading(true);

        try {
            // Get Auth token
            await login(email, password);
            setIsLoading(false);
            navigate("/home");
        
        } catch (error: any) {
            console.log(`Error: ${error}`);
            setErrorMessage(error.message);
            setIsLoading(false);
        }
      };

    return (
        <>
            <div>
                <h2>Login to TheDaily</h2>
                <div>
                    {isLoading && (
                        <span className="loading loading-spinner loading-lg"></span>
                    )}
                    <form className="signup-form-container" onSubmit={handleLogin}>
                        <div className="signup-input-container">
                            <label style={{ textAlign: 'left'}}>Email</label>
                            <input
                                className="signup-input"
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="signup-input-container">
                            <label style={{ textAlign: 'left'}}>Password</label>
                            <input
                                className="signup-input"
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                        {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
                        <div>
                            <button disabled={isLoading} className="bubble-button" type="submit">Login</button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    )
}