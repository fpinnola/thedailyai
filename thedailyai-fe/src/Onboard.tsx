import { useEffect, useState } from "react";

const newsCategories: string[] = ["economy", "business", "technology", "biotech", "software", "healthcare", "politics"];

export default function Onboard() {
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
            <h2>What types of news are you interested in?</h2>
            {categorySelections.map(elem => {
                return (
                    <button className={elem.selected ? "selected" : ""} onClick={() => selectedCategory(elem.name)}>{elem.name}</button>
                )
            })}
        </>
    )
}