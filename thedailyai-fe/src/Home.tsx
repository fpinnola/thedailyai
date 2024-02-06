import { useEffect, useState } from "react";
import { getNews, getPodcast } from "./external/news_be.external";
import StoryCard from "./components/StoryCard";

const USER_ID_TEST = 'frank123';

export default function Home() {

    const [articles, setArticles] = useState<any[]>([]);

    const [podcastAudioURL, setPodcastAudioURL] = useState('');

    // const [podcastScript, setPodcastScript] = useState('');

    // const fetchDailyPodcast = async (preferences: any) => {
    //     console.log(`Sending preferences: ${JSON.stringify(preferences)}`);
        
    //     let podcastURL: string = await getPodcast(preferences);
    //     console.log(`Got podcastURL: ${podcastURL}`);
    //     setPodcastAudioURL(podcastURL);
    // }

    useEffect(() => {
        // TODO: get articles from backend
        const wrapper = async () => {
            let prefString = localStorage.getItem('preferences');
            if (!prefString) return;
            const preferences = JSON.parse(prefString)
            preferences.userId = USER_ID_TEST;
            let news: any[] = await getNews(preferences);
            console.log(`${news.length} articles`)
            setArticles(news);
            // fetchDailyPodcast(preferences);
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
            <h3>Your News for {getDate()}</h3>
            {/* {!podcastAudioURL.length ? null : (
                <div>
                    <h4>Your daily podcast</h4>
                    <audio controls>
                        <source src={podcastAudioURL} type="audio/mpeg" />
                    </audio>
                </div>
            )} */}
            <div className="slider-container">
                {articles.map((elem, index) => (
                    <StoryCard key={elem.title + index} title={elem.title} summary={elem.summary} />
                    // <div>
                    //     <h4>{elem.title}</h4>
                    //     <p>{elem.summary}</p>
                    //     <a href={elem.url}>Read more</a>
                    // </div>
                ) )}
            </div>
        </>
    )
}