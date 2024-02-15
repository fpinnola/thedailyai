import { useEffect, useState } from "react";
import { getNews } from "./external/news_be.external";
import StoryCard from "./components/StoryCard";
import loading from "./assets/loading.gif"

const USER_ID_TEST = 'frank123';

const newsLoadingMessages = [
    "Gathering news from the cosmos...",
    "Orchestrating the symphony of headlines...",
    "Deciphering the scrolls of knowledge...",
    "Sifting through the sands of stories for you...",
    "Plucking your personalized petals from the news nebula...",
    "Assembling your anthology of the age's adventures...",
    "Brewing your morning news espresso...",
    "Tuning the antennas for your news frequency...",
    "Polishing the headlines just for you...",
    "Rounding up the news hounds for the latest scoop...",
    "Adjusting our news lenses to your perspective...",
    "Stirring the pot of today's tastiest tales...",
    "Filtering the noise to tune into your news...",
    "Cherry-picking today's news nuggets for you...",
    "Dusting off the day's top stories for your desk...",
    "Serving up a personalized plate of the daily buzz..."
];

export default function Home() {

    const [articles, setArticles] = useState<any[]>([]);
    const [loadingNews, setLoadingNews] = useState(false);
    const [loadingMessage] = useState( newsLoadingMessages[Math.floor(Math.random() * newsLoadingMessages.length)]);

    useEffect(() => {
        const wrapper = async () => {
            let prefString = localStorage.getItem('preferences');
            if (!prefString) return;
            const preferences = JSON.parse(prefString)
            preferences.userId = USER_ID_TEST;
            setLoadingNews(true);
            let news: any[] = await getNews(preferences);
            setLoadingNews(false);
            console.log(`${news.length} articles`)
            setArticles(news);
        }

        wrapper();

    }, []);

    const getDate = () => {
        const months = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
        const now = new Date();
        const month = months[now.getMonth()];
        const day = now.getDate();
        const year = now.getFullYear();

        return `${month} ${day}, ${year}`;
    }

    return (
        <>
            <div style={{
                position: 'absolute',
                top: 50,
                width: '100%',
                left: 0
            }}>
                <h4 style={{
                    textAlign: 'center',
                    opacity: 0.6
                }}>Your News for {getDate()}</h4>
            </div>
            {loadingNews && (
                <div style={{
                    display: 'flex',
                    height: '100vh',
                    width: '100%',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexDirection: 'column'
                }}>
                <img style={{
                    height: 24, 
                    width: 24
                }} src={loading} alt="Loading..." />
                <h3>{loadingMessage}</h3>
                </div>

            )}
            {!loadingNews && (
                <div className="slider-container">
                    {articles.map((elem, index) => (
                        <StoryCard key={elem.title + index} title={elem.title} summary={elem.summary} url={elem.url} />
                    ) )}
                </div>
            )}

        </>
    )
}