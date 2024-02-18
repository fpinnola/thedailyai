import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, signupUser, updateUserPreferences } from "./external/news_be.external";
import loading from "./assets/loading.gif"

const newsCategories: string[] = ["business", "technology", "politics", "healthcare", "legal", "science"];
const summaryDetailOptions: string[] = ["High-Level Overview", "Moderately Detailed", "Very Detailed"];
// const newsStyleOptions: string[] = ["Newscaster", "Humorous", "Serious", "Relaxed"];
const PAGES = 3;


export default function Onboard() {
    const navigate = useNavigate();
    const [categorySelections, setCategorySelections] = useState<any[]>([]);
    const [summaryDetail, setSummaryDetail] = useState<string>('');
    // const [selectedNewsStyle, setSelectedNewsStyle] = useState<string>('');
    const [page, setPage] = useState(0);

    useEffect(() => {
        const categories = newsCategories.map((elem) => {
            return { name: elem, selected: false };
        });
        setCategorySelections(categories);
    }, []);

    const selectedCategory = (category: string) => {
        const newCatetories = categorySelections.map(elem => {
            if (elem.name === category) {
                return {...elem, selected: !elem.selected};
            }
            return elem;
        });
        setCategorySelections(newCatetories);
    }

    

    const continueBtn = async () => {
        if (page + 1 >= PAGES) {
            // DONE, navigate to home
            const preferences = {
                categories: categorySelections.filter((elem) => elem.selected).map(elem => elem.name),
                summaryDetail: summaryDetail,
                // style: selectedNewsStyle
            };
            await updateUserPreferences(preferences);
            localStorage.setItem('preferences', JSON.stringify(preferences));
            navigate("/home");
            return;
        }

        setPage(page + 1);
    }

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSignup = async (event: any) => {
        event.preventDefault();
        
        // Check if passwords match
        if (password !== confirmPassword) {
          setErrorMessage('Passwords do not match.');
          return;
        }
    
        // Construct the request payload
        setIsLoading(true);
        try {
            const response = await signupUser(email, password);

            setErrorMessage('');
            localStorage.setItem('user', JSON.stringify(response));

            // Get Auth token
            const response2: any = await login(email, password);

            const token = response2.access_token;
            localStorage.setItem('access_token', JSON.stringify(token));
            setIsLoading(false);
            setPage(page + 1);

        } catch (error: any) {
            console.log(`Error: ${error}`);
            setErrorMessage(error.message);
            setIsLoading(false);
        }
      };
    

    if (page === 0) {
        return (
            <>
                <div>
                    <h2>Welcome to TheDaily. Create an account for free to get started</h2>

                    <div>
                        {isLoading && (
                            <img style={{
                                height: 24, 
                                width: 24
                            }} src={loading} alt="Loading..." />
                        )}
                        <form className="signup-form-container" onSubmit={handleSignup}>
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
                            <div className="signup-input-container">
                                <label style={{ textAlign: 'left'}}>Confirm Password</label>
                                <input
                                    type="password"
                                    className="signup-input"
                                    placeholder="Confirm Password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    required
                                />
                            </div>
                            {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
                            <div>
                                <button disabled={isLoading} className="bubble-button" type="submit">Continue</button>
                            </div>
                        </form>
                    </div>
                </div>
            </>
        )
    }
    else if (page === 1) {
        return (
            <>
                <div>
                    <h2>What types of news are you interested in?</h2>
                    <div>
                        {categorySelections.map(elem => {
                            return (
                                <button key={elem.name} className={"bubble-button " + (elem.selected ? "selected" : "unselected")} onClick={() => selectedCategory(elem.name)}>{elem.name}</button>
                            )
                        })}
                    </div>
                    <button className="bubble-button" onClick={continueBtn}>Continue</button>
                </div>
            </>
        )
    } else if (page === 2) {
        return (
            <>
                <div>
                    <h2>How detailed would you like your news summaries to be?</h2>
                    <div>
                        {summaryDetailOptions.map(elem => {
                            return (
                                <button key={elem} className={"bubble-button " + (elem === summaryDetail ? "selected" : "unselected")} onClick={() => setSummaryDetail(elem)}>{elem}</button>
                            )
                        })}
                    </div>
                    <button className="bubble-button" disabled={!summaryDetail.length} onClick={continueBtn}>Continue</button>
                </div>
            </>
        )
    } else {
        return (
        <>
            <div>
                <h2>Sorry there is a problem.</h2>
            </div>
        </>
        )
    }


}