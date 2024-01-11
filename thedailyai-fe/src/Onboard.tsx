import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const newsCategories: string[] = ["economy", "business", "technology", "biotech", "healthcare", "politics", "law", "government", "crime", "weather"];

export default function Onboard() {
    const navigate = useNavigate();
    const [categorySelections, setCategorySelections] = useState<any[]>([]);

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

    return (
        <>
            <div>
                <h2>What types of news are you interested in?</h2>
                <div>
                    {categorySelections.map(elem => {
                        return (
                            <button className={elem.selected ? "selected" : "unselected"} onClick={() => selectedCategory(elem.name)}>{elem.name}</button>
                        )
                    })}
                </div>
                <button onClick={() => navigate("/home")}>Done</button>
            </div>
        </>
    )
}