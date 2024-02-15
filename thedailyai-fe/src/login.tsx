import { useState } from "react";
import { login } from "./external/news_be.external";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleLogin = async (event: any) => {
        event.preventDefault();
        
        
        try {

            // Get Auth token
            const response: any = await login(email, password);

            const token = response.access_token;
            localStorage.setItem('access_token', JSON.stringify(token));
          
            navigate("/home");
        
        } catch (error: any) {
            console.log(`Error: ${error}`);
            setErrorMessage(error.message);
        }
      };

    return (
        <>
            <div>
                <h2>Welcome to TheDaily. Create an account for free to get started</h2>
                <div>
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
                            <button className="bubble-button" type="submit">Login</button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    )
}