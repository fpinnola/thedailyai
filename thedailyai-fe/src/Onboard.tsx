import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const newsCategories: string[] = ["economy", "business", "technology", "biotech", "healthcare", "politics", "law", "government", "crime", "weather"];
const summaryDetailOptions: string[] = ["High-Level Overview", "Moderately Detailed", "Very Detailed"];
const newsStyleOptions: string[] = ["Newscaster", "Humorous", "Serious", "Relaxed"];
const PAGES = 3;


export default function Onboard() {
    const navigate = useNavigate();
    const [categorySelections, setCategorySelections] = useState<any[]>([]);
    const [summaryDetail, setSummaryDetail] = useState<string>('');
    const [selectedNewsStyle, setSelectedNewsStyle] = useState<string>('');
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

    

    const continueBtn = () => {
        if (page + 1 >= PAGES) {
            // DONE, navigate to home
            const preferences = {
                categories: categorySelections.filter((elem) => elem.selected).map(elem => elem.name),
                summaryDetail: summaryDetail,
                style: selectedNewsStyle
            };
            localStorage.setItem('preferences', JSON.stringify(preferences));
            navigate("/home");
            return;
        }

        setPage(page + 1);
    }

    if (page === 0) {
        return (
            <>
                <div>
                    <h2>What types of news are you interested in?</h2>
                    <div>
                        {categorySelections.map(elem => {
                            return (
                                <button key={elem.name} className={elem.selected ? "selected" : "unselected"} onClick={() => selectedCategory(elem.name)}>{elem.name}</button>
                            )
                        })}
                    </div>
                    <button onClick={continueBtn}>Continue</button>
                </div>
            </>
        )
    } else if (page === 1) {
        return (
            <>
                <div>
                    <h2>How detailed would you like your news summaries to be?</h2>
                    <div>
                        {summaryDetailOptions.map(elem => {
                            return (
                                <button key={elem} className={elem === summaryDetail ? "selected" : "unselected"} onClick={() => setSummaryDetail(elem)}>{elem}</button>
                            )
                        })}
                    </div>
                    <button disabled={!summaryDetail.length} onClick={continueBtn}>Continue</button>
                </div>
            </>
        )
    } else if (page === 2) {
        return (
            <>
                <div>
                    <h2>What style would you like your news to be delivered in?</h2>
                    <div>
                        {newsStyleOptions.map(elem => {
                            return (
                                <button key={elem} className={selectedNewsStyle === elem ? "selected" : "unselected"} onClick={() => setSelectedNewsStyle(elem)}>{elem}</button>
                            )
                        })}
                    </div>
                    <button disabled={!selectedNewsStyle.length} onClick={continueBtn}>Continue</button>
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